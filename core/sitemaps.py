from django.contrib.sitemaps import Sitemap

from .models import Announcement


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    protocol = "https"

    def items(self):
        return ["home", "about", "services", "announcements", "contact"]

    def location(self, item):
        from django.urls import reverse
        return reverse(item)


class AnnouncementSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Announcement.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.published_at
