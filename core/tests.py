from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.urls import reverse

from .models import Announcement, ContactMessage
from .themes import get_theme


class PublicPagesTests(TestCase):
    def test_public_pages_render(self):
        for name in ["home", "about", "services", "announcements", "contact"]:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_unpublished_announcement_is_hidden(self):
        Announcement.objects.create(title="پیش‌نویس", slug="draft", body="...", is_published=False)
        response = self.client.get(reverse("announcement_detail", args=["draft"]))
        self.assertEqual(response.status_code, 404)

    def test_published_announcement_is_visible(self):
        Announcement.objects.create(title="فراخوان", slug="call-1", body="متن", is_published=True)
        response = self.client.get(reverse("announcement_detail", args=["call-1"]))
        self.assertEqual(response.status_code, 200)

    def test_robots_and_sitemap(self):
        self.assertIn(b"Sitemap:", self.client.get("/robots.txt").content)
        self.assertEqual(self.client.get("/sitemap.xml").status_code, 200)

    def test_healthz(self):
        self.assertEqual(self.client.get("/healthz/").json(), {"status": "ok"})


class ContactFormTests(TestCase):
    valid = {"name": "علی", "email": "ali@example.com", "phone": "", "message": "سلام", "website": ""}

    def test_valid_submission_is_saved(self):
        response = self.client.post(reverse("contact"), self.valid)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_honeypot_blocks_bots(self):
        data = dict(self.valid, website="http://spam.example")
        response = self.client.post(reverse("contact"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_invalid_email_is_rejected(self):
        response = self.client.post(reverse("contact"), dict(self.valid, email="not-an-email"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)


class ThemeTests(TestCase):
    def test_unknown_theme_raises(self):
        with self.assertRaises(ImproperlyConfigured):
            get_theme("does-not-exist")

    def test_theme_colors_reach_the_page(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "--primary:")
