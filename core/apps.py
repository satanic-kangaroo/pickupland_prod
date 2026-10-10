from django.apps import AppConfig
from django.db.backends.signals import connection_created


def _sqlite_pragmas(sender, connection, **kwargs):
    if connection.vendor != "sqlite":
        return
    cursor = connection.cursor()
    # WAL: خواندن و نوشتن هم‌زمان بهتر؛ foreign key ها فعال؛ همگام‌سازی سبک‌تر برای سرعت
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("PRAGMA synchronous = NORMAL;")


class CoreConfig(AppConfig):
    name = "core"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        connection_created.connect(_sqlite_pragmas)
