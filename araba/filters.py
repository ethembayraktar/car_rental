import django_filters
from django_filters import CharFilter, DateFilter, NumberFilter, UUIDFilter

from araba.models import Araba


class ArabaFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    ofis = UUIDFilter(field_name='name')
    vehicle_plate = CharFilter(field_name='vehicle_plate', lookup_expr='icontains')
    vehicle_register_seri = CharFilter(field_name='vehicle_register_seri', lookup_expr='icontains')
    vehicle_register_no = CharFilter(field_name='vehicle_register_no', lookup_expr='icontains')
    vehicle_type = NumberFilter(field_name="vehicle_type")
    car_mark = NumberFilter(field_name="car_mark")
    car_model = NumberFilter(field_name="car_model")
    car_model_year = NumberFilter(field_name="car_model_year")
    transmission = CharFilter(field_name='transmission', lookup_expr='icontains')
    fuel = CharFilter(field_name='fuel', lookup_expr='icontains')
    deposit = NumberFilter(field_name="deposit")
    mileage = NumberFilter(field_name="mileage")
    age = NumberFilter(field_name="age")
    cost_of_rental = NumberFilter(field_name="cost_of_rental")

    km_min_constraint = NumberFilter(field_name="km_min_constraint")
    age_min_constraint = NumberFilter(field_name="age_min_constraint")
    licence_min_constraint = NumberFilter(field_name="licence_min_constraint")
    payment_constraint = CharFilter(field_name='payment_constraint', lookup_expr='icontains')

    from_date = DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Araba
        fields = []
