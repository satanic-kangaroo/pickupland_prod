from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.urls import reverse

from .models import Announcement, ContactMessage, Course, JobOpening, Service
from .themes import get_theme

PUBLIC_PAGES = ["home", "about", "services", "academy", "membership", "hiring", "announcements", "contact"]


class PublicPagesTests(TestCase):
    def test_public_pages_render(self):
        for name in PUBLIC_PAGES:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_unpublished_announcement_is_hidden(self):
        Announcement.objects.create(title="پیش‌نویس", slug="draft", body="...", is_published=False)
        self.assertEqual(self.client.get(reverse("announcement_detail", args=["draft"])).status_code, 404)

    def test_robots_and_sitemap(self):
        self.assertIn(b"Sitemap:", self.client.get("/robots.txt").content)
        self.assertEqual(self.client.get("/sitemap.xml").status_code, 200)

    def test_healthz(self):
        self.assertEqual(self.client.get("/healthz/").json(), {"status": "ok"})


class ContentTests(TestCase):
    def test_course_pillars_are_shown_on_academy_page(self):
        course = Course.objects.create(code="FABSTART", title="t", summary="s", full_price=20_000_000,
                                       student_price=6_000_000, other_price=8_000_000)
        course.pillars.create(title="Enter The Fab", description="d", order=0)
        response = self.client.get(reverse("academy"))
        self.assertContains(response, "Enter The Fab")
        self.assertEqual(course.student_percent, 30)
        self.assertEqual(course.other_percent, 40)

    def test_open_jobs_are_listed(self):
        JobOpening.objects.create(title="طراح RF", track="RF", description="d", requirements="الف\nب")
        response = self.client.get(reverse("hiring"))
        self.assertContains(response, "طراح RF")

    def test_service_points_are_split_into_lines(self):
        service = Service(title="s", description="d", points="یک\n\nدو\n")
        self.assertEqual(service.points_list, ["یک", "دو"])

    def test_membership_page_lists_stages(self):
        self.assertEqual(self.client.get(reverse("membership")).status_code, 200)


class ContactFormTests(TestCase):
    valid = {"name": "علی", "email": "ali@example.com", "phone": "", "topic": "membership",
             "funding_stage": "seed", "message": "سلام", "website": ""}

    def test_valid_submission_is_saved_with_topic(self):
        response = self.client.post(reverse("contact"), self.valid)
        self.assertEqual(response.status_code, 302)
        saved = ContactMessage.objects.get()
        self.assertEqual(saved.topic, "membership")
        self.assertEqual(saved.funding_stage, "seed")

    def test_honeypot_blocks_bots(self):
        response = self.client.post(reverse("contact"), dict(self.valid, website="http://spam.example"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_invalid_email_is_rejected_with_aria(self):
        response = self.client.post(reverse("contact"), dict(self.valid, email="bad"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'aria-invalid="true"')
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_topic_is_prefilled_from_query(self):
        response = self.client.get(reverse("contact"), {"topic": "academy"})
        self.assertContains(response, 'value="academy" selected')


class AnnouncementTests(TestCase):
    def setUp(self):
        for i in range(12):
            Announcement.objects.create(title=f"فراخوان {i}", slug=f"call-{i}", body="متن")

    def test_list_is_paginated(self):
        self.assertEqual(len(self.client.get(reverse("announcements")).context["page_obj"]), 10)
        self.assertEqual(len(self.client.get(reverse("announcements"), {"page": 2}).context["page_obj"]), 2)

    def test_invalid_page_falls_back(self):
        self.assertEqual(self.client.get(reverse("announcements"), {"page": "abc"}).status_code, 200)

    def test_detail_has_newsarticle_jsonld(self):
        self.assertContains(self.client.get(reverse("announcement_detail", args=["call-1"])),
                            '"@type": "NewsArticle"')

    def test_nav_marks_current_page(self):
        self.assertContains(self.client.get(reverse("academy")), 'aria-current="page"')


class ThemeTests(TestCase):
    def test_unknown_theme_raises(self):
        with self.assertRaises(ImproperlyConfigured):
            get_theme("does-not-exist")

    def test_theme_colors_reach_the_page(self):
        self.assertContains(self.client.get(reverse("home")), "--primary:")


class SeedCommandTests(TestCase):
    def test_seed_loads_full_content(self):
        from django.core.management import call_command
        from .models import ProcessStep, Stat, TechField

        call_command("seed_pickupland", verbosity=0)
        self.assertEqual(TechField.objects.count(), 4)
        self.assertEqual(Service.objects.count(), 5)
        self.assertEqual(ProcessStep.objects.count(), 4)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.get(code="FABSTART").pillars.count(), 4)
        self.assertEqual(JobOpening.objects.count(), 3)
        self.assertEqual(Announcement.objects.count(), 4)
        self.assertEqual(Stat.objects.count(), 4)

    def test_seed_is_idempotent(self):
        from django.core.management import call_command
        from .models import CoursePillar

        call_command("seed_pickupland", verbosity=0)
        call_command("seed_pickupland", verbosity=0)
        self.assertEqual(TechField.objects.count(), 4)
        self.assertEqual(CoursePillar.objects.count(), 4)
        self.assertEqual(Announcement.objects.count(), 4)

    def test_reset_keeps_contact_messages(self):
        from django.core.management import call_command

        call_command("seed_pickupland", verbosity=0)
        ContactMessage.objects.create(name="x", email="x@example.com", message="m")
        call_command("seed_pickupland", "--reset", verbosity=0)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(TechField.objects.count(), 4)

    def test_fabstart_prices_are_correct(self):
        from django.core.management import call_command

        call_command("seed_pickupland", verbosity=0)
        course = Course.objects.get(code="FABSTART")
        self.assertEqual(course.full_price, 20_000_000)
        self.assertEqual(course.student_percent, 30)
        self.assertEqual(course.other_percent, 40)
