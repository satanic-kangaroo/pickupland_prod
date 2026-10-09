from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Announcement, ProcessStep, Service, TechField

FIELDS = [
    ("AI", "هوش مصنوعی", "توسعه‌ی مدل‌ها و کاربرد هوش مصنوعی در صنعت", "ai"),
    ("MW", "میکروالکترونیک", "طراحی تراشه و مدارهای مجتمع", "chip"),
    ("PH", "فوتونیک", "فناوری‌های مبتنی بر نور و ارتباطات نوری", "photon"),
    ("QT", "کوانتوم", "پژوهش و توسعه در فناوری‌های کوانتومی", "quantum"),
]

SERVICES = [
    ("حمایت از ایده و سرمایه‌گذاری", "جذب سرمایه برای ایده‌های ناب و همراهی در مسیر تجاری‌سازی.", "spark"),
    ("منتورینگ و آموزش", "مشاوره با منتورهای تخصصی و کارگاه در مدل کسب‌وکار، بازاریابی و توسعه‌ی محصول.", "mentor"),
    ("آزمایشگاه و پشتیبانی فنی", "تسهیلات آزمایشگاهی، تجهیزات پیشرفته و پشتیبانی فنی برای پروژه‌های پژوهشی.", "lab"),
    ("شبکه‌سازی", "ارتباط تیم‌ها با صنایع، دانشگاه‌ها و سرمایه‌گذاران در یک زیست‌بوم فعال.", "network"),
    ("مشاوره‌ی نوآوری", "شناسایی فرصت‌های بازار، ارزیابی ایده و طراحی مدل کسب‌وکار.", "consult"),
    ("تأمین مالی", "شناسایی منابع مناسب، از وام و سرمایه‌گذاری خطرپذیر تا کمک‌های دولتی.", "finance"),
]

STEPS = [
    ("ثبت‌نام", "فرم عضویت را تکمیل کرده و مدارک تیم یا شرکت خود را ارسال کنید."),
    ("ارزیابی", "تیم ارزیابی پیک آپ مدارک و توان فنی شما را بررسی می‌کند."),
    ("ورود به حلقه", "پس از تأیید، وارد حلقه‌ی مگا شبکه می‌شوید و با تیم‌های دیگر همکاری می‌کنید."),
    ("بهره‌مندی", "از منتورینگ، آزمایشگاه، تأمین مالی و شبکه‌ی صنعتی استفاده کنید."),
]


class Command(BaseCommand):
    help = "داده‌ی اولیه‌ی سایت. آمارها عمداً خالی می‌مانند تا عددهای واقعی از پنل وارد شوند."

    def handle(self, *args, **options):
        for i, (code, title, description, icon) in enumerate(FIELDS):
            TechField.objects.update_or_create(
                code=code,
                defaults={"title": title, "description": description, "icon": icon, "order": i},
            )
        for i, (title, description, icon) in enumerate(SERVICES):
            Service.objects.update_or_create(
                title=title,
                defaults={"description": description, "icon": icon, "order": i},
            )
        for i, (title, description) in enumerate(STEPS):
            ProcessStep.objects.update_or_create(
                title=title, defaults={"description": description, "order": i}
            )
        Announcement.objects.update_or_create(
            slug="fabstart",
            defaults={
                "title": "فراخوان دوره‌ی FABSTART",
                "summary": "دوره‌ی ورود به دنیای Fab و طراحی تراشه",
                "body": "متن کامل فراخوان را از پنل مدیریت ویرایش کنید.",
                "published_at": timezone.now(),
            },
        )
        self.stdout.write(self.style.SUCCESS("داده‌ی اولیه ثبت شد."))
        self.stdout.write("عددهای نمایشی (آمار) را از پنل مدیریت با مقادیر واقعی وارد کنید.")
