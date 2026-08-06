FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    zlib1g \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SECRET_KEY=build-only-not-for-runtime \
    DJANGO_DEBUG=false \
    DJANGO_ALLOWED_HOSTS=localhost

RUN python manage.py collectstatic --noinput

CMD python manage.py migrate --noinput && \
    exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT}" \
    --workers 2 \
    --threads 4 \
    --timeout 60
