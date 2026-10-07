import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def sample_celery_task(name="Quiz User"):
    """
    Celery to'g'ri sozlanganligini tekshirish uchun sinov vazifasi.
    """
    message = f"Salom {name}! Celery asinxron vazifasi muvaffaqiyatli bajarildi."
    logger.info(message)
    return message


@shared_task
def send_quiz_reminder_task(user_id):
    """
    Foydalanuvchiga quiz eslatmasini asinxron yuborish (namuna vazifa).
    """
    from django.contrib.auth.models import User
    try:
        user = User.objects.get(id=user_id)
        msg = f"Eslatma: {user.username} foydalanuvchisi uchun quiz xabari yuborildi."
        logger.info(msg)
        return msg
    except User.DoesNotExist:
        msg = f"Xatolik: ID={user_id} foydalanuvchi topilmadi."
        logger.warning(msg)
        return msg
