from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from araba.models import VehicleType, CarMark, CarModel, Araba


class VehicleTypeAdmin(admin.ModelAdmin):
    search_fields = ("id", "name",)


class CarMarkAdmin(admin.ModelAdmin):
    search_fields = ("id", "name",)


class CarModelAdmin(admin.ModelAdmin):
    search_fields = ("id", "name",)


class ArabaAdmin(admin.ModelAdmin):
    search_fields = ('id', 'vehicle_plate', 'car_mark', 'car_model', "vehicle_type",)
    list_display = ('id', 'vehicle_plate', 'car_mark', 'car_model', "vehicle_type",)

    model = Araba
    fieldsets = (
        (
            _("General Info"), {
                "fields": (
                    "ofis",
                    "name",
                    "vehicle_plate",
                    "vehicle_register_seri",
                    "vehicle_register_no",
                    "vehicle_type",
                    "car_mark",
                    "car_model",
                    "car_model_year",
                    "transmission",
                    "fuel",
                    "deposit",
                    "mileage",
                    "age",
                    "cost_of_rental"
                )}),
        (
            _("Constraints"),
            {
                "fields": (
                    "km_min_constraint",
                    "age_min_constraint",
                    "licence_min_constraint",
                    "payment_constraint",
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


admin.site.register(VehicleType, VehicleTypeAdmin)
admin.site.register(CarMark, CarMarkAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Araba, ArabaAdmin)
