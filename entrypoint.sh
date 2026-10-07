#!/bin/bash
set -e

# Ma'lumotlar bazasi tayyor bo'lishini tekshirish
if [ -n "$DB_HOST" ]; then
  echo "PostgreSQL ($DB_HOST:${DB_PORT:-5432}) tayyor bo'lishi kutilmoqda..."
  while ! python -c "import socket; s = socket.socket(); s.settimeout(1); s.connect(('$DB_HOST', int('${DB_PORT:-5432}'))); s.close()" 2>/dev/null; do
    sleep 0.5
  done
  echo "PostgreSQL tayyor va ulandi!"
fi

# Agar veb-server ishga tushirilayotgan bo'lsa: migratsiyalar va boshlang'ich ma'lumotlarni sozlash
if [[ "$*" == *"runserver"* ]] || [[ "$*" == *"gunicorn"* ]]; then
  echo "Ma'lumotlar bazasi migratsiyalari bajarilmoqda..."
  python manage.py migrate --noinput

  echo "Savollar bazaga yuklanmoqda..."
  python manage.py load_questions || true

  echo "Superadmin (sevinch / 123) tekshirilmoqda..."
  python manage.py setup_admin || true

  echo "Statik fayllar yig'ilmoqda..."
  python manage.py collectstatic --noinput || true
fi

exec "$@"
