from django.contrib import admin

from .models import (Announcement, ContactMessage, Course, CoursePillar, JobOpening,
                     ProcessStep, Service, Stat, TechField)


class CoursePillarInline(admin.TabularInline):
    model = CoursePillar
    extra = 0


@admin.register(TechField)
class TechFieldAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "icon", "order")
    list_editable = ("title", "order")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "schedule", "is_active", "order")
    list_editable = ("is_active", "order")
    inlines = [CoursePillarInline]


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ("title", "track", "is_open", "order")
    list_editable = ("is_open", "order")


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("label", "value", "order")
    list_editable = ("value", "order")


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "deadline", "published_at", "is_published")
    list_editable = ("is_published",)
    search_fields = ("title", "summary")
    date_hierarchy = "published_at"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "topic", "funding_stage", "email", "created_at", "is_handled")
    list_editable = ("is_handled",)
    list_filter = ("topic", "is_handled")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "phone", "topic", "funding_stage", "message", "created_at")
