from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from attachment.models import Attachment


class AttachmentAdmin(admin.ModelAdmin):
    search_fields = ('id', 'slug', 'mime')
    list_display = ('id', 'original_preview', 'thumbnail_preview', 'webp_preview', 'title', 'mime', 'created_at',
                    'created_by')
    model = Attachment
    fieldsets = (
        (
            _("General Info"), {
                "fields": (
                    'title',
                    'slug',
                    'mime',
                )}),
        (
            _("Files"),
            {
                "fields": (
                    'original',
                    'thumbnail',
                    'webp'
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
                    "deleted_at",
                    "updated_at",
                    "created_at",
                )}),
    )
    readonly_fields = ('deleted_at', 'updated_at', 'created_at')


admin.site.register(Attachment, AttachmentAdmin)
