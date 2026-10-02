from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Superadmin sevinch (parol: 123) foydalanuvchisini yaratish"

    def handle(self, *args, **options):
        username = 'sevinch'
        password = '123'
        email = 'sevinch@example.com'

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superadmin '{username}' muvaffaqiyatli yaratildi! (Parol: {password})"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superadmin '{username}' yangilandi va paroli o'rnatildi: {password}"))
