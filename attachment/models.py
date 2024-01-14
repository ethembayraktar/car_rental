import logging
import mimetypes
import os
import uuid

from PIL import Image
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from core.settings import MEDIA_ROOT, MEDIA_URL
from utils.models import BaseModel
from utils.util import validate_file_extension
import mimetypes


def get_file_path(instance, filename):
    ext = (filename.split('.')[-1]).lower()
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return f"attachments/{filename}"


class Attachment(models.Model):
    class Meta:
        verbose_name_plural = _('Attachments')
        verbose_name = _('Attachment')
        db_table = "attachment"
        ordering = ["-pk"]

    slug = models.CharField(max_length=255, blank=True, null=True)
    webp = models.FileField(upload_to="attachments/webp", blank=True, null=True, max_length=500)
    thumbnail = models.FileField(upload_to="attachments/thumbnails", blank=True, null=True, max_length=500)
    original = models.FileField(upload_to=get_file_path, validators=[validate_file_extension], blank=True,
                                null=True, max_length=500)
    title = models.CharField(max_length=500, blank=True, null=True)
    mime = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)

    created_by = models.ForeignKey('user.User', on_delete=models.RESTRICT, blank=True, null=True,
                                   related_name='created_by_%(class)s_related')
    updated_by = models.ForeignKey('user.User', on_delete=models.RESTRICT, blank=True, null=True,
                                   related_name='updated_by_%(class)s_related')
    deleted_by = models.ForeignKey('user.User', on_delete=models.RESTRICT, blank=True, null=True,
                                   related_name='deleted_by_%(class)s_related')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def save_webp_image(self, quality=70):
        image = Image.open(self.original)

        file_name = self.original.name
        file_name = file_name.replace("attachments", "").replace("/", "").replace("\\", "")
        webp_name, thumb_extension = os.path.splitext(file_name)
        image.save(fp=os.path.join(MEDIA_ROOT, "attachments", "webp", webp_name + ".webp"),
                   format="WEBP",
                   quality=quality)
        self.webp = f"attachments/webp/{webp_name}.webp"

    def make_thumbnail(self):
        if self.original is None:
            return
        try:
            mime_type, _ = mimetypes.guess_type(self.original.path)
            file_name = self.original.name
            file_name = file_name.replace("attachments", "").replace("/", "").replace("\\", "")
            thumb_name, thumb_extension = os.path.splitext(file_name)

            thumb_extension = thumb_extension.lower()

            if 'image' in mime_type:
                self.save_webp_image()
                image = Image.open(self.original)
                file_name = self.original.name
                file_name = file_name.replace("attachments", "").replace("/", "").replace("\\", "")
                file_name, file_extension = os.path.splitext(file_name)

                image.thumbnail((60, 60), Image.Resampling.LANCZOS)
                image.save(os.path.join(MEDIA_ROOT, "attachments", "thumbnails", thumb_name + ".png"), "PNG")
                self.thumbnail = f"attachments/thumbnails/{thumb_name}.png"
            elif thumb_extension in ['.pdf'] or 'pdf' in mime_type:
                self.thumbnail = 'attachments/thumbnails/mypdf.png'
            elif thumb_extension in ['.doc', '.docx'] or 'word' in mime_type:
                self.thumbnail = 'attachments/thumbnails/myword.png'
            elif thumb_extension in ['.xlsx', '.xls'] or 'xls' in mime_type or 'xlsx' in mime_type:
                self.thumbnail = 'attachments/thumbnails/myexcel.png'
            elif thumb_extension in ['.mp3', '.wav']:
                self.thumbnail = 'attachments/thumbnails/audio.png'
            elif thumb_extension in ['.mp4']:
                self.thumbnail = 'attachments/thumbnails/mp4.png'
            elif 'video' in mime_type:
                self.thumbnail = 'attachments/thumbnails/video.png'
            elif 'audio' in mime_type:
                self.thumbnail = 'attachments/thumbnails/audio.png'
            else:
                self.thumbnail = 'attachments/thumbnails/file.png'
        except Exception as e:
            logging.exception(e)

    def __str__(self):
        if self.webp:
            return f"{MEDIA_URL}{self.webp}"
        elif self.thumbnail:
            return f"{MEDIA_URL}{self.thumbnail}"
        elif self.original:
            return f"{MEDIA_URL}{self.original}"
        elif self.title:
            return self.title
        else:
            return str(self.pk)

    def save(self, *args, **kwargs):
        """
        If a new price is created, we make all the existing ones Inactive
        """

        self.make_thumbnail()
        super(Attachment, self).save(*args, **kwargs)

    raw_id_fields = ("id",)

    def image_preview(self):  # new
        if self.webp:
            return mark_safe(f'<img src = "{self.webp.url}" width="100"/>')
        elif self.thumbnail:
            return mark_safe(f'<img src = "{self.thumbnail.url}" width="100"/>')
        elif self.original:
            return mark_safe(f'<img src = "{self.original.url}" width="100"/>')
        else:
            return None

    def original_preview(self):
        if self.original:
            return mark_safe(f'<img src = "{self.original.url}" height="30"/>')
        else:
            return None

    def thumbnail_preview(self):
        if self.thumbnail:
            return mark_safe(f'<img src = "{self.thumbnail.url}" height="30"/>')
        else:
            return None

    def webp_preview(self):  # new
        if self.webp:
            return mark_safe(f'<img src = "{self.webp.url}" height="30"/>')
        else:
            return None
