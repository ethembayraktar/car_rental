from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from attachment.models import Attachment
from country.models import Il, Ilce, MahalleKoy, Sokak
from user.models import User
from utils.models import BaseModel
from utils.util import get_random_string


class Ofis(BaseModel):
    class Meta:
        verbose_name_plural = _('Ofices')
        verbose_name = _('Ofice')
        db_table = "ofis"
        ordering = ["-created_at"]

    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    logo = models.ForeignKey(Attachment, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ofis Adı')
    email = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ofis Kurumsal Eposta')
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ofis Kurumsal Telefon")

    il = models.ForeignKey(Il, blank=True, null=True, on_delete=models.CASCADE)
    ilce = models.ForeignKey(Ilce, blank=True, null=True, on_delete=models.CASCADE)
    mahallekoy = models.ForeignKey(MahalleKoy, blank=True, null=True, on_delete=models.CASCADE)
    sokak = models.ForeignKey(Sokak, blank=True, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, blank=True, null=True)
    code = models.CharField(max_length=4, blank=True, null=True, unique=True, verbose_name="Ofis Kodu")

    facebook = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ofis Facebook Adresi")
    twitter = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ofis Twitter Adresi")
    instagram = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ofis İnstagram Adresi")
    tiktok = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ofis Tiktok Adresi")

    latitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)

    def img_preview(self):  # new
        if self.logo and self.logo.webp:
            return mark_safe(f'<img src = "{self.logo.webp.url}" width="100"/>')
        elif self.logo and self.logo.thumbnail:
            return mark_safe(f'<img src = "{self.logo.thumbnail.url}" width="100"/>')
        elif self.logo and self.logo.original:
            return mark_safe(f'<img src = "{self.logo.original.url}" width="100"/>')
        else:
            return None

    def save(self, *args, **kwargs):
        is_new = self.id is None

        if is_new or self.code is None:
            code = None
            while True:
                code = get_random_string(4, "ABCDEF0123456789")
                if not Ofis.objects.filter(code=code).exists():
                    break

            self.code = code
        super(Ofis, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
