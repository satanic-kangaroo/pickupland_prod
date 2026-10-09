"""
تم‌های رنگی سایت. فقط مقادیر colors عوض می‌شوند؛ قالب‌ها و CSS هیچ رنگ ثابتی ندارند.
فعال‌سازی: PICKUP_THEME=night_fab  (در .env یا محیط اجرا)
"""
from django.core.exceptions import ImproperlyConfigured

THEMES = {
    # کاغذ نقشه‌ی مهندسی: زمینه‌ی روشن، جوهر تیره، آبی نقشه‌ای
    "blueprint": {
        "name": "نقشه‌ی مهندسی",
        "colors": {
            "bg": "#f3f1ea",
            "surface": "#faf9f4",
            "surface-2": "#ebe8de",
            "text": "#14181f",
            "muted": "#5b6371",
            "border": "#d3cdbd",
            "grid": "rgba(20, 24, 31, 0.06)",
            "primary": "#1f3a8a",
            "primary-contrast": "#faf9f4",
            "accent": "#b4530a",
        },
    },
    # اتاق آزمایشگاه شبانه
    "night_fab": {
        "name": "آزمایشگاه شبانه",
        "colors": {
            "bg": "#0c0f14",
            "surface": "#11161d",
            "surface-2": "#18202a",
            "text": "#e8ecf1",
            "muted": "#8b95a3",
            "border": "#263140",
            "grid": "rgba(232, 236, 241, 0.05)",
            "primary": "#7dd3fc",
            "primary-contrast": "#06121a",
            "accent": "#e5b25d",
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
