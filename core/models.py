from django.db import models
from django.urls import reverse
from django.utils import timezone


class TechField(models.Model):
    code = models.CharField("کد کوتاه", max_length=4, help_text="مثلاً AI یا MW")
    title = models.CharField("عنوان حوزه", max_length=100)
    description = models.TextField("توضیح")
    icon = models.CharField("آیکون", max_length=20, default="default",
                            help_text="یکی از: ai، chip، photon، quantum")
    order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "حوزه‌ی فناوری"
        verbose_name_plural = "حوزه‌های فناوری"

    def __str__(self):
        return f"{self.code} · {self.title}"


class Service(models.Model):
    title = models.CharField("عنوان خدمت", max_length=150)
    description = models.TextField("توضیح")
    icon = models.CharField("آیکون", max_length=20, default="default",
                            help_text="یکی از: spark، mentor، lab، network، consult، finance")
    order = models.PositiveSmallIntegerField("ترتیب", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"

    def __str__(self):
        return self.title


class ProcessStep(models.Model):
    title = models.CharField("عنوان مرحله", max_length=100)
    description = models.TextField("توضیح")
    order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "مرحله‌ی عضویت"
        verbose_name_plural = "مراحل عضویت"

    def __str__(self):
        return self.title


class Stat(models.Model):
    label = models.CharField("عنوان", max_length=100)
    value = models.CharField("مقدار (مثلاً ۵۰+)", max_length=20)
    order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "عدد نمایشی"
        verbose_name_plural = "اعداد نمایشی"

    def __str__(self):
        return f"{self.label}: {self.value}"


class Announcement(models.Model):
    title = models.CharField("عنوان", max_length=200)
    slug = models.SlugField("نامک", allow_unicode=True, unique=True, max_length=220,
                            help_text="انگلیسی یا فارسی، بدون فاصله؛ مثلاً fabstart-1405")
    summary = models.CharField("خلاصه", max_length=300, blank=True)
    body = models.TextField("متن کامل")
    deadline = models.DateField("مهلت ارسال", null=True, blank=True)
    published_at = models.DateTimeField("تاریخ انتشار", default=timezone.now)
    is_published = models.BooleanField("منتشر شود", default=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "فراخوان / خبر"
        verbose_name_plural = "فراخوان‌ها و اخبار"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("announcement_detail", args=[self.slug])


class ContactMessage(models.Model):
    name = models.CharField("نام", max_length=100)
    email = models.EmailField("ایمیل")
    phone = models.CharField("تلفن", max_length=20, blank=True)
    message = models.TextField("پیام")
    created_at = models.DateTimeField("زمان ارسال", auto_now_add=True)
    is_handled = models.BooleanField("پاسخ داده شد", default=False)

    class Meta:
        ordering = ["is_handled", "-created_at"]
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

    def __str__(self):
        return f"{self.name} · {self.created_at:%Y-%m-%d}"
