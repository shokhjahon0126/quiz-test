from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    number = models.PositiveIntegerField(unique=True, help_text="Savol asl raqami (1 dan 16 gacha)")
    question_text = models.TextField(help_text="Savol matni")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['number']
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        return f"Savol #{self.number}: {self.question_text[:50]}"


class GameCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_cards')
    card_number = models.PositiveIntegerField(help_text="Doskadagi kartochka raqami (1 dan 16 gacha)")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='assigned_cards')
    is_opened = models.BooleanField(default=False, help_text="Kartochka ochilganmi?")
    opened_at = models.DateTimeField(null=True, blank=True, help_text="Ochilgan vaqti")

    class Meta:
        unique_together = ('user', 'card_number')
        ordering = ['card_number']
        verbose_name = "O'yin kartochkasi"
        verbose_name_plural = "O'yin kartochkalari"

    def __str__(self):
        status = "Ochilgan" if self.is_opened else "Yopiq"
        return f"{self.user.username} - Karta #{self.card_number} ({status}) -> Savol #{self.question.number}"
