import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from quiz.models import Question


class Command(BaseCommand):
    help = "questions.json faylidan savollarni ma'lumotlar bazasiga yuklash"

    def handle(self, *args, **options):
        json_path = settings.BASE_DIR / 'questions.json'
        if not json_path.exists():
            self.stderr.write(self.style.ERROR(f"{json_path} fayli topilmadi!"))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        count = 0
        for item in data:
            q_id = item.get('id')
            q_text = item.get('question')
            if q_id is not None and q_text:
                Question.objects.update_or_create(
                    number=q_id,
                    defaults={'question_text': q_text}
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Muvaffaqiyatli yuklandi: {count} ta savol!"))
