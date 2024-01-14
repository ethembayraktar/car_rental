from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from slugify import slugify

from attachment.models import Attachment
from utils.models import BaseModel


class Kampanya(BaseModel):
    class Meta:
        verbose_name_plural = _('Campaign')
        verbose_name = _('Campaigns')
        db_table = "kampanya"
        ordering = ["-created_at"]

    title = models.CharField(max_length=400, blank=True, null=True, verbose_name="Kampanya Başlığı")
    order = models.IntegerField(blank=True, null=True, verbose_name="Öncelik Sırası")
    slug = models.CharField(max_length=500, blank=True, null=True, verbose_name="Slug")
    summary = CKEditor5Field(max_length=2500, blank=True, null=True, config_name='extends', verbose_name="Özet")
    details = CKEditor5Field(max_length=1500, blank=True, null=True, config_name='extends', verbose_name="Detay")
    banner = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE,
                               related_name='kampanya_banner', verbose_name="Kampanya Banner")

    started_at = models.DateTimeField(blank=True, null=True, verbose_name=_("Start At"))
    end_at = models.DateTimeField(blank=True, null=True, verbose_name=_("End At"))

    def save(self, *args, **kwargs):
        """
        If a new price is created, we make all the existing ones Inactive
        """
        if self.title:
            self.slug = slugify(self.title)
        super(Kampanya, self).save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else str(self.pk)
