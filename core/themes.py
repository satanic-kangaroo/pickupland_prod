"""
تم‌های رنگی سایت. فقط مقادیر colors عوض می‌شوند؛ قالب‌ها و CSS هیچ رنگ ثابتی ندارند.
فعال‌سازی: PICKUP_THEME=night_fab  (در .env یا محیط اجرا)
"""
from django.core.exceptions import ImproperlyConfigured

THEMES = {
    # اتاق تمیز: سفیدِ خنثی، آبیِ عمیق، مسی
    "clean_room": {
        "name": "اتاق تمیز",
        "colors": {
            "bg": "#eef1ec",
            "surface": "#fbfcfa",
            "surface-2": "#e2e8e1",
            "text": "#0b1a20",
            "muted": "#52636b",
            "border": "#c4cec8",
            "grid": "rgba(11, 26, 32, 0.07)",
            "primary": "#0a4a63",
            "primary-contrast": "#fbfcfa",
            "accent": "#d9662b",
            "ink": "#0b1a20",
            "ink-contrast": "#eef1ec",
        },
    },
    # کارگاه شبانه: نور فیروزه‌ای روی زمینه‌ی تیره
    "night_fab": {
        "name": "کارگاه شبانه",
        "colors": {
            "bg": "#061013",
            "surface": "#0b181d",
            "surface-2": "#12242b",
            "text": "#e8f5f2",
            "muted": "#8ea7a5",
            "border": "#1d3a41",
            "grid": "rgba(94, 224, 207, 0.06)",
            "primary": "#5ee0cf",
            "primary-contrast": "#04131a",
            "accent": "#ff9a4d",
            "ink": "#e8f5f2",
            "ink-contrast": "#061013",
        },
    },
}


def get_theme(name):
    try:
        return THEMES[name]
    except KeyError:
        raise ImproperlyConfigured(
            f"تم «{name}» تعریف نشده است. تم‌های موجود: {', '.join(THEMES)}"
        )
