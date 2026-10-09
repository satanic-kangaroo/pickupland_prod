# پیک آپ لند

## اجرای محلی (توسعه)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_pickupland
python manage.py createsuperuser
python manage.py runserver
```

تست‌ها: `python manage.py test core`

## استقرار (production)

1. فایل `.env` را از `.env.example` بسازید و مقادیر را پر کنید. حتماً `DJANGO_SECRET_KEY` را عوض کنید.
2. فونت را در `core/static/core/fonts/Vazirmatn-Variable.woff2` قرار دهید.
3. با Docker:
   ```bash
   docker compose up -d --build
   docker compose exec web python manage.py createsuperuser
   docker compose exec web python manage.py seed_pickupland
   ```
4. پشت یک reverse proxy (مثل Nginx یا Caddy) با HTTPS قرار دهید. مقدار `DJANGO_SECURE_SSL_REDIRECT=1` را فقط وقتی بگذارید که HTTPS فعال است.
5. Health check: `GET /healthz/` برای load balancer یا مانیتورینگ.

## تغییر تم

در `.env` یا محیط اجرا: `PICKUP_THEME=night_fab`. تم جدید را در `core/themes.py` اضافه کنید؛ هیچ قالب یا CSS ای نیاز به تغییر ندارد.

## محتوا

- حوزه‌ها، خدمات، مراحل عضویت، فراخوان‌ها، اعداد نمایشی و پیام‌های تماس: از پنل `/admin/`.
- اطلاعات تماس، نشانی و ساعت کاری: در `SITE_CONTACT` داخل `config/settings.py` (یا `SITE_PHONE` در `.env`).
- متن صفحه‌ی «درباره‌ی ما»: `core/templates/core/about.html`.

## کارهای باقی‌مانده پیش از لانچ

- عکس واقعی تیم، مجموعه و آزمایشگاه (به‌جای تزئینات فعلی)
- لوگوی رسمی و راهنمای برند
- اعداد واقعی برای بخش آمار
- بررسی حقوقی و تأیید متن‌ها توسط کارفرما
- تنظیم SMTP برای اعلان پیام‌های تماس
- نصب گواهی SSL و تنظیم دامنه
- پشتیبان‌گیری خودکار از Postgres
- ابزار تحلیل (مثلاً Plausible یا Matomo) با رعایت قوانین حریم خصوصی
