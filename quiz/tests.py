from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from quiz.models import Question, GameCard


class QuizAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'sevinch'
        self.password = '123'
        self.user = User.objects.create_superuser(
            username=self.username,
            password=self.password,
            email='sevinch@example.com'
        )

        # Create 16 test questions
        self.questions = []
        for i in range(1, 17):
            q = Question.objects.create(number=i, question_text=f"Test question #{i}")
            self.questions.append(q)

    def test_superuser_credentials(self):
        """sevinch / 123 orqali tizimga kirishni tekshirish"""
        login_success = self.client.login(username='sevinch', password='123')
        self.assertTrue(login_success)

    def test_anonymous_redirect_to_login(self):
        """Tizimga kirmagan foydalanuvchi login sahifasiga yo'naltirilishi kerak"""
        response = self.client.get(reverse('quiz_home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_login_page_renders_clean_without_credentials_or_superuser_info(self):
        """Login sahifasi toza bo'lishi: sevinch, 123 va Django Superuser ma'lumotlari olib tashlangan"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "sevinch")
        self.assertNotContains(response, "123")
        self.assertNotContains(response, "Django Superuser")
        self.assertNotContains(response, "Django Admin paneli")

    def test_quiz_home_shows_16_covered_cards_with_random_questions(self):
        """Asosiy sahifada 16 ta savol raqami ko'rinishi va random savollar biriktirilganligi"""
        self.client.login(username='sevinch', password='123')
        response = self.client.get(reverse('quiz_home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cards']), 16)
        
        # Barcha 16 ta kartochka bazada yaratilgan bo'lishi kerak
        cards = GameCard.objects.filter(user=self.user)
        self.assertEqual(cards.count(), 16)

        # Barchasi dastlab ochilmagan bo'lishi kerak
        for card in response.context['cards']:
            self.assertFalse(card['is_opened'])

    def test_open_question_once_and_block_second_time(self):
        """Kartochka bir marta ochiladi va ikkinchi marta tanlab bo'lmaydi"""
        self.client.login(username='sevinch', password='123')

        # Dastlabki sahifani yuklab kartalarni hosil qilamiz
        self.client.get(reverse('quiz_home'))

        # 5-kartochkaga qaysi savol biriktirilganini bilib olamiz
        card_5_before = GameCard.objects.get(user=self.user, card_number=5)

        # 1-marta ochish: muvaffaqiyatli
        response = self.client.post(reverse('open_question', kwargs={'question_number': 5}))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['number'], 5)
        self.assertEqual(data['question_text'], card_5_before.question.question_text)
        self.assertEqual(data['opened_count'], 1)
        self.assertEqual(data['remaining_count'], 15)

        # 2-marta o'sha savolni tanlash: rad etilishi kerak!
        response2 = self.client.post(reverse('open_question', kwargs={'question_number': 5}))
        self.assertEqual(response2.status_code, 400)
        data2 = response2.json()
        self.assertFalse(data2['success'])
        self.assertIn("allaqachon tanlangan", data2['error'])

        # Doskani qayta tekshirish
        home_res = self.client.get(reverse('quiz_home'))
        card_5 = next(c for c in home_res.context['cards'] if c['number'] == 5)
        self.assertTrue(card_5['is_opened'])

    def test_reset_quiz_reshuffles_randomly(self):
        """Doskani qayta boshlashda savollar qayta aralashtiriladi va barcha kartochkalar yopiladi"""
        self.client.login(username='sevinch', password='123')
        self.client.get(reverse('quiz_home'))

        # Bir nechta kartani ochamiz
        self.client.post(reverse('open_question', kwargs={'question_number': 1}))
        self.client.post(reverse('open_question', kwargs={'question_number': 2}))
        self.assertEqual(GameCard.objects.filter(user=self.user, is_opened=True).count(), 2)

        # Reset qilamiz
        response = self.client.post(reverse('reset_quiz'))
        self.assertEqual(response.status_code, 302)

        # Barcha kartochkalar yopilgan bo'lishi kerak
        self.assertEqual(GameCard.objects.filter(user=self.user, is_opened=True).count(), 0)
        self.assertEqual(GameCard.objects.filter(user=self.user, is_opened=False).count(), 16)

    def test_celery_sample_task(self):
        """Celery asinxron vazifalarini tekshirish"""
        from quiz.tasks import sample_celery_task, send_quiz_reminder_task
        res = sample_celery_task.apply(args=["TestUser"])
        self.assertEqual(res.status, 'SUCCESS')
        self.assertIn("TestUser", res.result)

        res2 = send_quiz_reminder_task.apply(args=[self.user.id])
        self.assertEqual(res2.status, 'SUCCESS')
        self.assertIn(self.username, res2.result)

