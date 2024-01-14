from django.db import models
from django.utils.translation import gettext_lazy as _

from ofis.models import Ofis
from utils.constants import MANUEL, AUTOMATIC, SEMI_AUTOMATIC, CONTINUOUSLY_VARIABLE, DUAL_CLUTCH, GASOLINE, DIESEL, \
    BIO_DIESEL, HYBRID, ELECTRIC, CREDIT_CARD, CASH
from utils.models import BaseModel2, BaseModel


class VehicleType(BaseModel2):
    class Meta:
        verbose_name_plural = _('Vehicle Types')
        verbose_name = _('Vehicle Type')
        db_table = 'vehicle_type'
        ordering = ["name"]

    name = models.CharField(max_length=250)

    raw_id_fields = ("name",)

    def __str__(self):
        return self.name


class CarMark(BaseModel2):
    class Meta:
        verbose_name_plural = _('Car Marks')
        verbose_name = _('Car Marks')
        db_table = 'car_mark'
        ordering = ["name"]

    name = models.CharField(max_length=250, unique=True, blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)

    raw_id_fields = ("name",)

    @classmethod
    def get_car_marks(cls):
        return [f"{c.name} - {c.code}" for c in CarMark.objects.all().order_by("name")]

    def save(self, *args, **kwargs):
        is_new = self.id is None

        super(CarMark, self).save(*args, **kwargs)

    def __str__(self):
        if self.code and self.name:
            return f"{self.code}-{self.name}"
        return self.name


class CarModel(BaseModel2):
    class Meta:
        verbose_name_plural = _('Car Models')
        verbose_name = _('Car Model')
        db_table = 'car_model'
        ordering = ["name"]
        unique_together = [["car_mark", "name", "code"]]

    car_mark = models.ForeignKey(CarMark, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    raw_id_fields = ("name",)

    def save(self, *args, **kwargs):
        is_new = self.id is None

        super(CarModel, self).save(*args, **kwargs)

    def __str__(self):
        if self.code and self.name:
            return f"{self.code}-{self.name}"
        return self.name


class Araba(BaseModel):
    class Meta:
        verbose_name_plural = _('Vehicles')
        verbose_name = _('Vehicle')
        db_table = "vehicle"
        ordering = ["pk"]

    TRANSMISSION_CHOICES = ((MANUEL, "Manuel"),
                            (AUTOMATIC, "Automatic"),
                            (SEMI_AUTOMATIC, "Semi Automatic"),
                            (CONTINUOUSLY_VARIABLE, "Continuously Variable"),
                            (DUAL_CLUTCH, "Dual Clutch"),
                            )

    FUEL_TYPES = ((GASOLINE, "Gasoline"),
                  (DIESEL, "Diesel"),
                  (BIO_DIESEL, "Bio Diesel"),
                  (HYBRID, "Hybrid"),
                  (ELECTRIC, "Electric")
                  )
    PAYMENT_CHOICES = ((CREDIT_CARD, "Credit Card"),
                       (CASH, "Cash")
                       )
    name = models.CharField(max_length=255, blank=True, null=True)
    ofis = models.ForeignKey(Ofis, blank=True, null=True, on_delete=models.DO_NOTHING)
    vehicle_plate = models.CharField(max_length=10, blank=True, null=True)
    vehicle_register_seri = models.CharField(max_length=2, blank=True, null=True)
    vehicle_register_no = models.CharField(max_length=6, blank=True, null=True)
    vehicle_type = models.ForeignKey(VehicleType, blank=True, null=True, on_delete=models.DO_NOTHING)
    car_mark = models.ForeignKey(CarMark, blank=True, null=True, on_delete=models.DO_NOTHING)
    car_model = models.ForeignKey(CarModel, blank=True, null=True, on_delete=models.DO_NOTHING)
    car_model_year = models.IntegerField(blank=True, null=True)
    transmission = models.CharField(max_length=50, blank=True, null=True, choices=TRANSMISSION_CHOICES)
    fuel = models.CharField(max_length=50, blank=True, null=True, choices=FUEL_TYPES)
    deposit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    mileage = models.FloatField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    cost_of_rental = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    km_min_constraint = models.IntegerField(blank=True, null=True)
    age_min_constraint = models.IntegerField(blank=True, null=True)
    licence_min_constraint = models.IntegerField(blank=True, null=True)
    payment_constraint = models.CharField(blank=True,
                                          null=True, choices=PAYMENT_CHOICES, max_length=20,
                                          default=CREDIT_CARD)

    def save(self, *args, **kwargs):
        if self.ofis and self.vehicle_type and self.car_mark and self.car_model:
            self.name = (f"{self.ofis.name} /  {self.vehicle_type.name} /  {self.car_mark.name} / "
                         f" {self.car_model.name}")

        if self.vehicle_plate:
            self.vehicle_plate = self.vehicle_plate.replace(" ", "").upper()
        super(Araba, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle_plate}"
