from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from country.models import Il, Ilce, MahalleKoy, Sokak


class IlAdminConfig(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")
    model = Il
    fieldsets = (
        (
            _("Il Info"), {
                "fields": (
                    "name",
                    "is_active",
                    "is_deleted",
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
    readonly_fields = ("created_at", "deleted_at", "updated_at",)


class IlceAdminConfig(admin.ModelAdmin):
    list_display = ("id", "name", "il")
    search_fields = ("id", "name", "il__name")
    model = Ilce
    fieldsets = (
        (
            _("Il Info"), {
                "fields": (
                    "name",
                    "is_active",
                    "is_deleted",
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
    readonly_fields = ("created_at", "deleted_at", "updated_at",)


class MahalleKoyAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "ilce__name", "il__name")


class SokakAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "mahallkoy__name", "ilce__name", "il__name")





admin.site.register(Il, IlAdminConfig)
admin.site.register(Ilce, IlceAdminConfig)
admin.site.register(MahalleKoy, MahalleKoyAdmin)
admin.site.register(Sokak, SokakAdmin)

