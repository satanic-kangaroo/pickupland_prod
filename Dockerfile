FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# collectstatic فقط برای ساخت image است؛ کلید واقعی در زمان اجرا از محیط خوانده می‌شود
RUN DJANGO_SECRET_KEY=build-only DJANGO_DEBUG=0 python manage.py collectstatic --noinput

RUN useradd --create-home appuser && mkdir -p /app/data && chown -R appuser:appuser /app/data
USER appuser
VOLUME ["/app/data"]

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile -"]
