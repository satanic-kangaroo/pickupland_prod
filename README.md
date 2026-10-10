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

در `.env` یا محیط اجرا: `PICKUP_THEME=night_fab` (تم پیش‌فرض: `clean_room`). تم جدید را در `core/themes.py` اضافه کنید؛ هیچ قالب یا CSS ای نیاز به تغییر ندارد.

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


## صفحات سایت

| مسیر | صفحه |
|---|---|
| `/` | صفحه‌ی اصلی (هیرو، حوزه‌ها، خدمات، آکادمی، عضویت، فراخوان‌ها) |
| `/خدمات/` | خدمات توسعه‌ی نوآوری |
| `/آکادمی/` | دوره‌های FABSTART و FABINSIGHT با هزینه و یارانه |
| `/عضویت/` | ساختار حلقه، مراحل عضویت، دسته‌های همکار |
| `/طراحی-تراشه/` | فراخوان جذب طراح مدار مجتمع |
| `/فراخوان‌ها/` | فهرست و جزئیات فراخوان‌ها و اخبار |
| `/درباره-ما/` | مأموریت و برنامه‌های راهبردی |
| `/تماس-با-ما/` | فرم تماس با موضوع و مرحله‌ی سرمایه‌گذاری |

## بعد از تغییر مدل‌ها

مدل‌ها تغییر کرده‌اند، پس مایگریشن جدید لازم است:

```bash
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_pickupland
```

اگر دیتابیس قبلی را دارید و می‌خواهید از نو شروع کنید، آن را پاک کنید و دوباره migrate کنید؛ داده‌ی اولیه از seed می‌آید.

## منابع محتوا

محتوای صفحات از سایت رفرنس استخراج شده است: معرفی پیک آپ، خدمات، شرایط عضویت حلقه، جزئیات دوره‌ی FABSTART و فراخوان جذب طراح تراشه. متن‌های قالبی سایت رفرنس (مثل «لورم ایپسوم» و «بیش از ۱۰۰۰۰ مشتری خوشحال») عمداً وارد نشده‌اند.


## دیتابیس: SQLite

دیتابیس فعلاً SQLite است و فایل آن در `data/db.sqlite3` قرار می‌گیرد (در Docker همان مسیر `/app/data` است و روی هاست bind شده تا با ری‌استارت پاک نشود).

- پشتیبان‌گیری: کافی است فایل `data/db.sqlite3` را کپی کنید. چون WAL فعال است، همراه آن فایل‌های `-wal` و `-shm` هم ممکن است باشند؛ بهتر است سرویس را لحظه‌ی کپی متوقف کنید یا از دستور `sqlite3 db.sqlite3 ".backup backup.sqlite3"` استفاده کنید.
- با ۳ worker گونیکورن، نوشتن‌های هم‌زمان در SQLite صف می‌شوند؛ برای ترافیک فعلی کاملاً کافی است.
- مهاجرت به Postgres در آینده: فقط تنظیمات `DATABASES` عوض می‌شود و `dumpdata` / `loaddata` داده را منتقل می‌کند.
