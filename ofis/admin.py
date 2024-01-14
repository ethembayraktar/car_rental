from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ofis.models import Ofis


class OfisAdminConfig(admin.ModelAdmin):
    list_display = ("img_preview", "code", "name", "email", "phone", "address")
    search_fields = ("id", "code", "name", "email", "phone", "address")
    model = Ofis
    fieldsets = (
        (
            _("General Info"), {
                "fields": (
                    "code",
                    "user",
                    "logo",
                    "name",
                    "email",
                    "phone",
                    "is_active",
                    "is_deleted",
                )}),
        (
            _("Adress Info"),
            {
                "fields": (
                    "il",
                    "ilce",
                    "mahallekoy",
                    "sokak",
                    "address",
                    "latitude",
                    "longitude",
                )}),
        (
            _("Social Media"),
            {
                "fields": (
                    "facebook",
                    "twitter",
                    "instagram",
                    "tiktok",
                )}),
        (
            _("Important People"),
            {
                "fields": (
                    "created_by",
                    "updated_by",
                    "deleted_by"
                )}),

        (
            _("Important dates"),
            {
                "fields": (
                    "deleted_at",
                    "updated_at",
                    "created_at"
                )}),
    )
    readonly_fields = ("code", "created_at", "deleted_at", "updated_at",)


admin.site.register(Ofis, OfisAdminConfig)

