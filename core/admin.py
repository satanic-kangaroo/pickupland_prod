from django.contrib import admin

from .models import Announcement, ContactMessage, ProcessStep, Service, Stat, TechField


@admin.register(TechField)
class TechFieldAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "icon", "order")
    list_editable = ("title", "order")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order", "is_active")
    list_editable = ("order", "is_active")


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
    list_display = ("name", "email", "phone", "created_at", "is_handled")
    list_editable = ("is_handled",)
    list_filter = ("is_handled",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "phone", "message", "created_at")
