import json
import logging

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .forms import ContactForm
from .models import (Announcement, ContactMessage, Course, JobOpening, ProcessStep,
                     Service, Stat, TechField)

logger = logging.getLogger(__name__)

CONTACT_LIMIT = 5
CONTACT_WINDOW = 60 * 60
ANNOUNCEMENTS_PER_PAGE = 10

# پنج دسته‌ی عضو حلقه، طبق صفحه‌ی «عضویت در مگا شبکه»
MEMBER_TYPES = [
    ("انجمن‌ها", "انجمن‌های فعال در حوزه‌ی فناوری که می‌توانند بخشی از مگا شبکه باشند."),
    ("مراکز تحقیقاتی دانشگاهی", "مراکزی که امکان انجام پروژه‌های مرتبط با صنعت را دارند."),
    ("سرمایه‌گذاران خطرپذیر", "مجموعه‌هایی که امکان سرمایه‌گذاری خطرپذیر را دارند."),
    ("رویدادهای نوآورانه", "رویدادهایی که دارای شبکه‌ی همکاری هستند و در حلقه حضور دارند."),
    ("شبکه‌های همکار", "سایر شبکه‌هایی که تمایل به همکاری با پیک آپ دارند."),
]

TEAM_FIELDS = ["هوش مصنوعی", "یادگیری ماشین", "رباتیک", "اینترنت اشیا", "بیوتکنولوژی", "طراحی تراشه"]


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _jsonld(data):
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def home(request):
    return render(request, "core/home.html", {
        "fields": TechField.objects.all(),
        "services": Service.objects.filter(is_active=True),
        "course": Course.objects.filter(is_active=True, code="FABSTART").prefetch_related("pillars").first(),
        "steps": ProcessStep.objects.all(),
        "stats": Stat.objects.all(),
        "announcements": Announcement.objects.filter(is_published=True)[:3],
        "open_jobs": JobOpening.objects.filter(is_open=True).count(),
    })


def about(request):
    return render(request, "core/about.html", {"fields": TechField.objects.all()})


def services(request):
    return render(request, "core/services.html", {
        "services": Service.objects.filter(is_active=True),
    })


def academy(request):
    courses = Course.objects.filter(is_active=True).prefetch_related("pillars")
    return render(request, "core/academy.html", {"courses": courses})


def membership(request):
    return render(request, "core/membership.html", {
        "steps": ProcessStep.objects.all(),
        "member_types": MEMBER_TYPES,
        "team_fields": TEAM_FIELDS,
    })


def hiring(request):
    return render(request, "core/hiring.html", {
        "jobs": JobOpening.objects.filter(is_open=True),
    })


def announcement_list(request):
    queryset = Announcement.objects.filter(is_published=True)
    page_obj = Paginator(queryset, ANNOUNCEMENTS_PER_PAGE).get_page(request.GET.get("page"))
    return render(request, "core/announcement_list.html", {"page_obj": page_obj})


def announcement_detail(request, slug):
    item = get_object_or_404(Announcement, slug=slug, is_published=True)
    article = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": item.title,
        "description": item.summary or item.title,
        "datePublished": item.published_at.isoformat(),
        "url": f"{settings.SITE_URL}{item.get_absolute_url()}",
        "publisher": {"@type": "Organization", "name": settings.SITE_CONTACT["name"]},
    }
    return render(request, "core/announcement_detail.html", {
        "item": item,
        "article_jsonld": _jsonld(article),
    })


def _notify_team(message):
    body = (
        f"موضوع: {message.get_topic_display()}\n"
        f"مرحله‌ی سرمایه‌گذاری: {message.get_funding_stage_display() or '-'}\n"
        f"نام: {message.name}\n"
        f"ایمیل: {message.email}\n"
        f"تلفن: {message.phone or '-'}\n\n"
        f"{message.message}"
    )
    try:
        send_mail(
            f"[{message.get_topic_display()}] پیام از {message.name}",
            body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_NOTIFY_EMAIL],
        )
    except Exception:
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

        for name in form.errors:
            form.fields[name].widget.attrs.update({
                "aria-invalid": "true",
                "aria-describedby": f"error-{name}",
            })
    else:
        topic = request.GET.get("topic", "")
        valid_topics = dict(ContactMessage.TOPIC_CHOICES)
        form = ContactForm(initial={"topic": topic if topic in valid_topics else "other"})
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
