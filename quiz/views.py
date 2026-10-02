import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Question, GameCard


def get_or_create_game_cards(user):
    """
    Foydalanuvchiga tegishli 16 ta kartochkani oladi.
    Agar hali mavjud bo'lmasa, savollarni tasodifiy (random) aralashtirib kartochkalarni yaratadi.
    """
    cards = list(GameCard.objects.filter(user=user).select_related('question').order_by('card_number'))
    all_questions = list(Question.objects.all())

    # Agar kartochkalar hali yaratilmagan bo'lsa yoki savollar soniga teng bo'lmasa
    if len(cards) < len(all_questions) and len(all_questions) > 0:
        return shuffle_game_cards(user)

    return cards


def shuffle_game_cards(user):
    """
    Savollarni tasodifiy (random) aralashtirib, 16 ta kartochkaga qaytadan biriktiradi
    va barcha kartochkalarni yopiq holatga keltiradi.
    """
    questions = list(Question.objects.all())
    random.shuffle(questions)

    cards = []
    for card_idx, question in enumerate(questions, start=1):
        card, _ = GameCard.objects.update_or_create(
            user=user,
            card_number=card_idx,
            defaults={
                'question': question,
                'is_opened': False,
                'opened_at': None,
            }
        )
        cards.append(card)

    return sorted(cards, key=lambda c: c.card_number)


def login_view(request):
    """Foydalanuvchi tizimga kirish sahifasi."""
    if request.user.is_authenticated:
        return redirect('quiz_home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, "Iltimos, barcha maydonlarni to'ldiring!")
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Xush kelibsiz, {user.username}!")
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('quiz_home')
            else:
                messages.error(request, "Login yoki parol noto'g'ri kiritildi!")

    return render(request, 'quiz/login.html')


def logout_view(request):
    """Tizimdan chiqish."""
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('login')


@login_required
def quiz_home_view(request):
    """Asosiy Quiz doskasi - 16 ta savol kartochkasi."""
    cards = get_or_create_game_cards(request.user)

    card_list = []
    for card in cards:
        card_list.append({
            'number': card.card_number,
            'is_opened': card.is_opened,
        })

    total_count = len(cards)
    opened_count = sum(1 for c in cards if c.is_opened)
    remaining_count = max(0, total_count - opened_count)
    progress_percentage = int((opened_count / total_count * 100)) if total_count > 0 else 0

    context = {
        'cards': card_list,
        'total_count': total_count,
        'opened_count': opened_count,
        'remaining_count': remaining_count,
        'progress_percentage': progress_percentage,
    }
    return render(request, 'quiz/home.html', context)


@login_required
@require_POST
def open_question_view(request, question_number):
    """
    Kartochkani ochish API endpointi.
    Kartochka raqami (1..16) orqali unga biriktirilgan tasodifiy savolni ochadi.
    Agar ilgari ochilgan bo'lsa, qayta tanlashni rad etadi.
    """
    card = get_object_or_404(GameCard, user=request.user, card_number=question_number)

    if card.is_opened:
        return JsonResponse({
            'success': False,
            'error': f"#{question_number} raqamidagi savol allaqachon tanlangan! Qayta tanlash mumkin emas.",
            'number': card.card_number
        }, status=400)

    # Kartochkani ochilgan holatga o'tkazish
    card.is_opened = True
    card.opened_at = timezone.now()
    card.save(update_fields=['is_opened', 'opened_at'])

    total_count = GameCard.objects.filter(user=request.user).count()
    opened_count = GameCard.objects.filter(user=request.user, is_opened=True).count()
    remaining_count = max(0, total_count - opened_count)
    progress_percentage = int((opened_count / total_count * 100)) if total_count > 0 else 0

    return JsonResponse({
        'success': True,
        'number': card.card_number,
        'question_text': card.question.question_text,
        'total_count': total_count,
        'opened_count': opened_count,
        'remaining_count': remaining_count,
        'progress_percentage': progress_percentage
    })


@login_required
@require_POST
def reset_quiz_view(request):
    """
    Quiz doskasini qayta boshlash.
    Barcha 16 ta savol tasodifiy (random) tartibda qaytadan aralashtiriladi
    va barcha kartochkalar yopiq holatga keltiriladi.
    """
    shuffle_game_cards(request.user)
    messages.success(request, "Savollar tasodifiy (random) tarzda qayta joylashtirildi va doska yangilandi!")
    return redirect('quiz_home')
