from django.contrib import admin
from .models import Question, GameCard


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('number', 'short_question', 'created_at')
    ordering = ('number',)
    search_fields = ('question_text',)

    def short_question(self, obj):
        return obj.question_text[:80] + '...' if len(obj.question_text) > 80 else obj.question_text
    short_question.short_description = "Savol"


@admin.register(GameCard)
class GameCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'question_ref', 'is_opened', 'opened_at')
    list_filter = ('user', 'is_opened')
    ordering = ('user', 'card_number')
    search_fields = ('user__username', 'question__question_text')

    def question_ref(self, obj):
        return f"Savol #{obj.question.number}: {obj.question.question_text[:40]}"
    question_ref.short_description = "Biriktirilgan savol"
