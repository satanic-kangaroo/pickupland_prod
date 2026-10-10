from django.db import models
from django.urls import reverse
from django.utils import timezone


class TechField(models.Model):
    """چهار حوزه‌ی فعالیت مگا شبکه."""
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
    description = models.TextField("توضیح کوتاه")
    points = models.TextField("موارد خدمت", blank=True,
                              help_text="هر خط یک مورد؛ در صفحه‌ی خدمات به‌صورت فهرست نمایش داده می‌شود")
    icon = models.CharField("آیکون", max_length=20, default="default",
                            help_text="یکی از: spark، mentor، lab، network، consult، finance، market، academy")
    order = models.PositiveSmallIntegerField("ترتیب", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"

    def __str__(self):
        return self.title

    @property
    def points_list(self):
        return [line.strip() for line in self.points.splitlines() if line.strip()]


class Course(models.Model):
    """دوره‌های آکادمی؛ مثل FABSTART و FABINSIGHT."""
    code = models.CharField("کد دوره", max_length=20, unique=True, help_text="مثلاً FABSTART")
    title = models.CharField("عنوان", max_length=150)
    summary = models.TextField("معرفی دوره")
    level_label = models.CharField("سطح", max_length=60, blank=True, help_text="مثلاً «سطح اول · پیش‌نیاز»")
    duration = models.CharField("مدت", max_length=80, blank=True)
    schedule = models.CharField("زمان برگزاری", max_length=120, blank=True)
    location = models.CharField("محل برگزاری", max_length=255, blank=True)
    full_price = models.PositiveIntegerField("هزینه‌ی واقعی (تومان)", default=0,
                                             help_text="صفر یعنی اعلام نشده؛ در سایت «به‌زودی» نمایش داده می‌شود")
    student_price = models.PositiveIntegerField("هزینه برای دانشجویان تحصیلات تکمیلی (تومان)", default=0)
    other_price = models.PositiveIntegerField("هزینه برای سایر شرکت‌کنندگان (تومان)", default=0)
    subsidy_note = models.TextField("توضیح یارانه / حمایت", blank=True)
    extra_note = models.TextField("نکات تکمیلی", blank=True)
    is_active = models.BooleanField("فعال", default=True)
    order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "دوره‌ی آکادمی"
        verbose_name_plural = "دوره‌های آکادمی"

    def __str__(self):
        return self.code

    @property
    def has_price(self):
        return self.full_price > 0

    def _percent(self, value):
        return round(value * 100 / self.full_price) if self.full_price else 0

    @property
    def student_percent(self):
        return self._percent(self.student_price)

    @property
    def other_percent(self):
        return self._percent(self.other_price)


class CoursePillar(models.Model):
    """ارکان دوره؛ مثلاً Enter The Fab."""
    course = models.ForeignKey(Course, related_name="pillars", on_delete=models.CASCADE, verbose_name="دوره")
    title = models.CharField("عنوان رکن", max_length=100, help_text="مثلاً Enter The Fab")
    description = models.TextField("توضیح")
    order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "رکن دوره"
        verbose_name_plural = "ارکان دوره"

    def __str__(self):
        return f"{self.course.code} · {self.title}"


class JobOpening(models.Model):
    """فراخوان‌های استخدام، مثل طراح مدار مجتمع."""
    title = models.CharField("عنوان موقعیت", max_length=150)
    track = models.CharField("حوزه", max_length=60, help_text="مثلاً آنالوگ، دیجیتال یا RF")
    description = models.TextField("شرح کار")
    requirements = models.TextField("شرایط", help_text="هر خط یک مورد")
    is_open = models.BooleanField("باز است", default=True)
    order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "موقعیت شغلی"
        verbose_name_plural = "موقعیت‌های شغلی"

    def __str__(self):
        return self.title

    @property
    def requirements_list(self):
        return [line.strip() for line in self.requirements.splitlines() if line.strip()]


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
                            help_text="انگلیسی یا فارسی، بدون فاصله؛ مثلاً fabstart")
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
    TOPIC_CHOICES = [
        ("membership", "عضویت در مگا شبکه"),
        ("academy", "دوره‌های آکادمی"),
        ("hiring", "همکاری و استخدام"),
        ("services", "خدمات توسعه‌ی نوآوری"),
        ("other", "سایر موارد"),
    ]
    STAGE_CHOICES = [
        ("", "انتخاب نشده"),
        ("preseed", "Preseed"),
        ("seed", "Seed"),
        ("round1", "Round 1"),
        ("round2", "Round 2"),
        ("round3", "Round 3"),
    ]

    name = models.CharField("نام", max_length=100)
    email = models.EmailField("ایمیل")
    phone = models.CharField("تلفن", max_length=20, blank=True)
    topic = models.CharField("موضوع", max_length=20, choices=TOPIC_CHOICES, default="other")
    funding_stage = models.CharField("مرحله‌ی سرمایه‌گذاری", max_length=10, choices=STAGE_CHOICES, blank=True)
    message = models.TextField("پیام")
    created_at = models.DateTimeField("زمان ارسال", auto_now_add=True)
    is_handled = models.BooleanField("پاسخ داده شد", default=False)

    class Meta:
        ordering = ["is_handled", "-created_at"]
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

    def __str__(self):
        return f"{self.name} · {self.created_at:%Y-%m-%d}"
