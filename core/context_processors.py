import json

from django.conf import settings

from .themes import get_theme


def theme(request):
    active = get_theme(settings.PICKUP_THEME)
    return {
        "theme_name": settings.PICKUP_THEME,
        "theme_title": active["name"],
        "theme_vars": active["colors"],
    }


def site_info(request):
    contact = settings.SITE_CONTACT
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": contact["name"],
        "url": settings.SITE_URL,
        "email": contact["email"],
        "address": {"@type": "PostalAddress", "streetAddress": contact["address"], "addressCountry": "IR"},
    }
    # جلوگیری از بسته شدن زودهنگام تگ script
    org_json = json.dumps(org, ensure_ascii=False).replace("</", "<\\/")
    return {"site": contact, "site_url": settings.SITE_URL, "org_schema_json": org_json}
