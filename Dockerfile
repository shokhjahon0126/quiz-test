FROM python:3.12-slim

# Python muhit sozlamalari
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Loyiha ishchi katalogi
WORKDIR /app

# Tizim paketlari
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python kutubxonalarini o'rnatish
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Loyiha kodlarini nusxalash
COPY . /app/

# Entrypoint skriptiga ijro huquqini berish
RUN chmod +x /app/entrypoint.sh

# Standart port
EXPOSE 8000

# Entrypoint va birlamchi buyruq
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
