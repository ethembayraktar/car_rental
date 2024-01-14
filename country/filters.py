import django_filters
from django_filters import CharFilter, DateFilter, NumberFilter

from country.models import Il, Ilce, MahalleKoy, Sokak, CarModel, CarMark, VehicleType


class IlFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    from_date = DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Il
        fields = []


class IlceFilter(django_filters.FilterSet):
    il = NumberFilter(field_name='il')
    il_name = CharFilter(field_name='il__name', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    from_date = DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Ilce
        fields = []


class MahalleKoyFilter(django_filters.FilterSet):
    il = NumberFilter(field_name='il')
    ilce = NumberFilter(field_name='ilce')
    il_name = CharFilter(field_name='il__name', lookup_expr='icontains')
    ilce_name = CharFilter(field_name='ilce__name', lookup_expr='icontains')
    posta_kodu = CharFilter(field_name='posta_kodu', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = MahalleKoy
        fields = []


class SokakFilter(django_filters.FilterSet):
    il = NumberFilter(field_name='il')
    ilce = NumberFilter(field_name='ilce')
    mahallekoy = NumberFilter(field_name='mahallekoy')

    il_name = CharFilter(field_name='il__name', lookup_expr='icontains')
    ilce_name = CharFilter(field_name='ilce__name', lookup_expr='icontains')
    mahallekoy_name = CharFilter(field_name='mahallekoy__name', lookup_expr='icontains')

    name = CharFilter(field_name='name', lookup_expr='icontains')

    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Sokak
        fields = []


class CarMarkFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = CarMark
        fields = []


class CarModelFilter(django_filters.FilterSet):
    car_mark = NumberFilter(field_name='car_mark')
    car_mark_name = CharFilter(field_name='car_mark__name', lookup_expr='icontains')
    car_mark_code = CharFilter(field_name='car_mark__code', lookup_expr='exact')

    name = CharFilter(field_name='name', lookup_expr='icontains')

    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = CarModel
        fields = []


class VehicleTypeFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = VehicleType
        fields = []
