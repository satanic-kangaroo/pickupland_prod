import logging

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .forms import ContactForm
from .models import Announcement, ProcessStep, Service, Stat, TechField

logger = logging.getLogger(__name__)

CONTACT_LIMIT = 5          # حداکثر پیام از هر نشانی
CONTACT_WINDOW = 60 * 60   # در یک ساعت


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def home(request):
    return render(request, "core/home.html", {
        "fields": TechField.objects.all(),
        "services": Service.objects.filter(is_active=True)[:6],
        "steps": ProcessStep.objects.all(),
        "stats": Stat.objects.all(),
        "announcements": Announcement.objects.filter(is_published=True)[:4],
    })


def about(request):
    return render(request, "core/about.html", {"fields": TechField.objects.all()})


def services(request):
    return render(request, "core/services.html", {
        "services": Service.objects.filter(is_active=True),
    })


def announcement_list(request):
    return render(request, "core/announcement_list.html", {
        "announcements": Announcement.objects.filter(is_published=True),
    })


def announcement_detail(request, slug):
    item = get_object_or_404(Announcement, slug=slug, is_published=True)
    return render(request, "core/announcement_detail.html", {"item": item})


def _notify_team(message):
    body = (
        f"نام: {message.name}\n"
        f"ایمیل: {message.email}\n"
        f"تلفن: {message.phone or '-'}\n\n"
        f"{message.message}"
    )
    try:
        send_mail(
            f"پیام جدید از سایت: {message.name}",
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_NOTIFY_EMAIL],
        )
    except Exception:
        # پیام قبلاً در دیتابیس ذخیره شده؛ خطای ایمیل نباید کاربر را خراب کند
        logger.exception("ارسال اعلان پیام تماس %s ناموفق بود", message.pk)


def contact(request):
    if request.method == "POST":
        key = f"contact-rate:{_client_ip(request)}"
        attempts = cache.get(key, 0)
        if attempts >= CONTACT_LIMIT:
            messages.error(request, "تعداد پیام‌ها از این نشانی زیاد است. کمی بعد دوباره تلاش کنید.")
            return redirect("contact")

        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            cache.set(key, attempts + 1, CONTACT_WINDOW)
            _notify_team(message)
            messages.success(request, "پیام شما ثبت شد. تیم پیک آپ به زودی با شما تماس می‌گیرد.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


def not_found(request, exception=None):
    return render(request, "404.html", status=404)


@require_GET
def robots(request):
    body = "User-agent: *\nDisallow: /admin/\nAllow: /\n\nSitemap: {}{}\n".format(
        settings.SITE_URL, reverse("sitemap")
    )
    return HttpResponse(body, content_type="text/plain; charset=utf-8")


@require_GET
def healthz(request):
    try:
        connection.ensure_connection()
    except Exception:
        logger.exception("healthz: دیتابیس در دسترس نیست")
        return JsonResponse({"status": "error"}, status=503)
    return JsonResponse({"status": "ok"})
