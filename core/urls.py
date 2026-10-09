from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import views
from .sitemaps import AnnouncementSitemap, StaticSitemap

sitemaps = {"static": StaticSitemap, "announcements": AnnouncementSitemap}

urlpatterns = [
    path("", views.home, name="home"),
    path("درباره-ما/", views.about, name="about"),
    path("خدمات/", views.services, name="services"),
    path("فراخوان‌ها/", views.announcement_list, name="announcements"),
    path("فراخوان‌ها/<str:slug>/", views.announcement_detail, name="announcement_detail"),
    path("تماس-با-ما/", views.contact, name="contact"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", views.robots, name="robots"),
    path("healthz/", views.healthz, name="healthz"),
]
