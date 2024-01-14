import decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from slugify import slugify

from attachment.models import Attachment
from utils.models import BaseModel, BaseModel2


class Frontend(BaseModel2):
    class Meta:
        verbose_name_plural = _('Frontend')
        verbose_name = _('Frontend')
        db_table = "frontend"
        ordering = ["-created_at"]

    site_name = models.CharField(_("Site Name"), max_length=255, blank=True, null=True)
   
    panel_login_bg = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='panel_login_bg')
    logo = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE, related_name='logo',
                             verbose_name="Site Logosu")
    ajax_loading = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE,
                                     related_name='ajax_loading',
                                     verbose_name="Ajax Yükleniyor Gif")
   
    favicon = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE, related_name='favicon',
                                verbose_name="Favicon")
    commission_reference_rate = models.DecimalField(default=decimal.Decimal(10.0), max_digits=10, decimal_places=2,
                                                    blank=True, null=True)
    memnun_musteri = models.IntegerField(blank=True, null=True)
    yol_yardim = models.IntegerField(blank=True, null=True)
    hizmet = models.IntegerField(blank=True, null=True)
    hizmet_noktasi = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    sub_title = models.CharField(max_length=255, blank=True, null=True)
    add_video = models.CharField(max_length=255, blank=True, null=True)
    short_text = CKEditor5Field('Short Text', max_length=2500, blank=True, null=True, config_name='extends')
    text = CKEditor5Field('Text', max_length=1500, blank=True, null=True, config_name='extends')
    contact_image = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='contact_image')
    footer_image = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE,
                                     related_name='footer_image')
    image1 = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE, related_name='image1')
    image2 = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE, related_name='image2')
    image_add_video = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE,
                                        related_name='image_add_video')

    address = models.CharField(max_length=500, blank=True, null=True)
    phone1 = models.CharField(max_length=20, blank=True, null=True)
    phone2 = models.CharField(max_length=20, blank=True, null=True)
    email1 = models.CharField(max_length=100, blank=True, null=True)
    email2 = models.CharField(max_length=100, blank=True, null=True)

    linkedin = models.CharField(max_length=500, blank=True, null=True)
    instagram = models.CharField(max_length=500, blank=True, null=True)
    youtube = models.CharField(max_length=500, blank=True, null=True)
    facebook = models.CharField(max_length=500, blank=True, null=True)
    tiktok = models.CharField(max_length=500, blank=True, null=True)
    twitter = models.CharField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        If a new price is created, we make all the existing ones Inactive
        """
        if self.title:
            self.slug = slugify(self.title)
        super(Frontend, self).save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else str(self.pk)


class Seo(BaseModel2):
    class Meta:
        verbose_name_plural = _('Seo')
        verbose_name = _('Seo')
        db_table = "seo"
        ordering = ["-created_at"]

    url = models.CharField(max_length=255, primary_key=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    copyright = models.CharField(max_length=255, blank=True, null=True)
    geo_position = models.CharField(max_length=255, default="39.91248393130924, 32.77162300696531")
    geo_region = models.CharField(max_length=255, default="TR-06")
    geo_placename = models.CharField(max_length=255, default="Mustafa Kemal Mah. 2142 Cad. Lütfiye Hanım Apt. "
                                                             "No:8/9 Çankaya Ankara")
    robots = models.CharField(max_length=255, blank=True, null=True)
    twitter_card = models.CharField(max_length=255, default=None, blank=True, null=True)
    twitter_site = models.CharField(max_length=255, default=None, blank=True, null=True)
    twitter_title = models.CharField(max_length=255, default=None, blank=True, null=True)
    twitter_description = models.CharField(max_length=255, default=None, blank=True, null=True)
    twitter_creator = models.CharField(max_length=255, default=None, blank=True, null=True)
    twitter_image = models.CharField(max_length=255, default=None, blank=True, null=True)
    twitter_data1 = models.CharField(max_length=255, default=None, blank=True, null=True)
    twitter_label1 = models.CharField(max_length=255, default=None, blank=True, null=True)
    twitter_data2 = models.CharField(max_length=255, default=None, blank=True, null=True)
    twitter_label2 = models.CharField(max_length=255, default=None, blank=True, null=True)
    og_price_amount = models.CharField(max_length=255, blank=True, null=True)
    og_price_currency = models.CharField(max_length=255, default=None, blank=True, null=True)
    og_site_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    og_description = models.CharField(max_length=255, default=None, blank=True, null=True)
    og_image = models.CharField(max_length=255, default=None, blank=True, null=True)
    og_url = models.CharField(max_length=255, default=None, blank=True, null=True)
    og_type = models.CharField(max_length=255, default=None, blank=True, null=True)
    og_title = models.CharField(max_length=255, default=None, blank=True, null=True)
    googlebot = models.CharField(max_length=255, default=None, blank=True, null=True)
    googlebot_news = models.CharField(max_length=255, default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        If a new price is created, we make all the existing ones Inactive
        """
        if self.title:
            self.slug = slugify(self.title)
        super(Seo, self).save(*args, **kwargs)

    def __str__(self):
        return self.url
