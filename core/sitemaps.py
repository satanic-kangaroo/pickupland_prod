from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Announcement


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    protocol = "https"

    def items(self):
        return ["home", "about", "services", "academy", "membership", "hiring", "announcements", "contact"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "home" else 0.7


class AnnouncementSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Announcement.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at
