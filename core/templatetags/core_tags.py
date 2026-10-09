import jdatetime
from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe

register = template.Library()

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

ICONS = {
    "ai": '<circle cx="5" cy="6" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="12" cy="12" r="2"/>'
          '<circle cx="19" cy="6" r="2"/><circle cx="19" cy="18" r="2"/>'
          '<path d="M7 6.5l3 4.5M7 17.5l3-4.5M14 11l3-4M14 13l3 4"/>',
    "chip": '<rect x="7" y="7" width="10" height="10" rx="1.5"/>'
            '<path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    "photon": '<path d="M4 18L11 6l9 12z"/><path d="M1.5 11.5h5M14 11l7 1.5"/>',
    "quantum": '<circle cx="12" cy="12" r="2"/><ellipse cx="12" cy="12" rx="9" ry="4"/>'
               '<ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(60 12 12)"/>'
               '<ellipse cx="12" cy="12" rx="9" ry="4" transform="rotate(-60 12 12)"/>',
    "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',
    "mentor": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 11l2 2 4-4"/>',
    "lab": '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M7.5 15h9"/>',
    "network": '<circle cx="12" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/>'
               '<path d="M12 7v4M12 11l-5 6M12 11l5 6"/>',
    "consult": '<path d="M4 5h16v11H9l-5 4z"/>',
    "finance": '<path d="M3 20h18"/><path d="M6 16V10M12 16V6M18 16v-4"/>',
    "default": '<circle cx="12" cy="12" r="8"/>',
}


@register.simple_tag
def icon(name):
    body = ICONS.get(name, ICONS["default"])
    return mark_safe(
        '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
        f"{body}</svg>"
    )


@register.filter
def fa_num(value):
    return str(value).translate(FA_DIGITS)


@register.filter
def jdate(value, fmt="%Y/%m/%d"):
    if not value:
        return ""
    if hasattr(value, "hour") and timezone.is_aware(value):
        value = timezone.localtime(value)
    if hasattr(value, "hour"):
        value = value.replace(tzinfo=None)
        jalali = jdatetime.datetime.fromgregorian(datetime=value)
    else:
        jalali = jdatetime.date.fromgregorian(date=value)
    return jalali.strftime(fmt).translate(FA_DIGITS)
