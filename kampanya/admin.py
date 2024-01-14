from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from kampanya.models import Kampanya


class KampanyaAdmin(admin.ModelAdmin):
    search_fields = ('id', 'slug', 'title', 'summary', 'details')
    list_display = ('id', "title", 'slug', 'summary', 'started_at', 'end_at', 'created_at', 'is_active', 'is_deleted')

    model = Kampanya
    fieldsets = (
        (
            _("General Settings"), {
                "fields": (
                    "slug",
                    "title",
                    "order",
                    "summary",
                    "details",
                    "is_active",
                    "is_deleted",
                )}),
        (
            _("Images & Videos"),
            {
                "fields": (
                    "banner",
                )}),
        (
            _("Important People"),
            {
                "fields": (
                    "deleted_by",
                    "updated_by",
                    "created_by",
                )}),
        (
            _("Important Dates"),
            {
                "fields": (
                    "started_at",
                    "end_at",
                    "deleted_at",
                    "updated_at",
                    "created_at",
                )}),
    )
    readonly_fields = ('slug', 'deleted_at', 'updated_at', 'created_at')


admin.site.register(Kampanya, KampanyaAdmin)
