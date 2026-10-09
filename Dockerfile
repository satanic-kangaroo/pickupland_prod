FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# collectstatic فقط برای ساخت image است؛ کلید واقعی در زمان اجرا از محیط خوانده می‌شود
RUN DJANGO_SECRET_KEY=build-only DJANGO_DEBUG=1 python manage.py collectstatic --noinput

COPY . .

# اول کاربر رو بساز
RUN useradd --create-home appuser

# مالکیت کل /app رو به appuser بده
RUN chown -R appuser:appuser /app

# حالا کاربر رو عوض کن
USER appuser

# collectstatic با کاربر appuser اجرا می‌شه
RUN DJANGO_SECRET_KEY=build-only DJANGO_DEBUG=1 python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --access-logfile -"]
