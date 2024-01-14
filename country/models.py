from django.db import models

from utils.constants import MAHALLE, KOY
from utils.models import BaseModel2


class Il(BaseModel2):
    class Meta:
        verbose_name_plural = 'İller'
        verbose_name = 'İl'
        db_table = "il"
        ordering = ["name"]

    name = models.CharField(max_length=250)
    long_min = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat_min = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    long_max = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat_max = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    raw_id_fields = ("name",)

    def __str__(self):
        return self.name


class Ilce(BaseModel2):
    class Meta:
        verbose_name_plural = 'İlçeler'
        verbose_name = 'İlçe'
        db_table = "ilce"
        ordering = ["name"]

    name = models.CharField(max_length=250)
    il = models.ForeignKey(Il, on_delete=models.CASCADE)

    long_min = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat_min = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    long_max = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat_max = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    raw_id_fields = ("name",)

    def __str__(self):
        return self.name


class MahalleKoy(BaseModel2):
    class Meta:
        verbose_name_plural = 'Mahalle/Köyler'
        verbose_name = 'Mahalle/Köy'
        db_table = "mahallekoy"
        ordering = ["ilce", "name"]

    TYPE = ((MAHALLE, 'mahalle'),
            (KOY, 'koy'))

    name = models.CharField(max_length=250)
    il = models.ForeignKey(Il, blank=True, null=True, on_delete=models.CASCADE)
    ilce = models.ForeignKey(Ilce, blank=True, null=True, on_delete=models.CASCADE)
    semt_bucak_belde = models.CharField(max_length=255, blank=True, null=True)
    posta_kodu = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, default=MAHALLE, choices=TYPE)

    long_min = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat_min = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    long_max = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat_max = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    raw_id_fields = ("pk",)

    def __str__(self):
        if self.semt_bucak_belde and self.ilce:
            return f"{self.pk}. {self.name} / {self.semt_bucak_belde} / {self.ilce.name}"
        if self.semt_bucak_belde:
            return f"{self.pk}. {self.name} / {self.semt_bucak_belde}"
        elif self.ilce:
            return f"{self.pk}. {self.name} / {self.ilce.name}"
        elif self.name:
            return f"{self.pk}. {self.name}"
        return self.pk


class Sokak(BaseModel2):
    class Meta:
        verbose_name_plural = 'Sokaklar'
        verbose_name = 'Sokak'
        db_table = "sokak"
        ordering = ["il", "ilce", "mahallekoy", "name"]

    TYPE = ((MAHALLE, 'mahalle'),
            (KOY, 'koy'))

    name = models.CharField(max_length=250)
    il = models.ForeignKey(Il, blank=True, null=True, on_delete=models.CASCADE)
    ilce = models.ForeignKey(Ilce, blank=True, null=True, on_delete=models.CASCADE)
    mahallekoy = models.ForeignKey(MahalleKoy, blank=True, null=True, on_delete=models.CASCADE)

    long_min = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat_min = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    long_max = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lat_max = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    raw_id_fields = ("pk",)

    def __str__(self):
        if self.name:
            return f"{self.pk}. {self.name}"
        return self.pk
