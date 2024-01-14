import django_filters
from django_filters import DateFilter, NumberFilter, UUIDFilter, CharFilter

from ofis.models import Ofis


class OfisFilter(django_filters.FilterSet):
    user = NumberFilter(field_name='user', lookup_expr='exact')
    logo = UUIDFilter(field_name='logo', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    email = CharFilter(field_name='email', lookup_expr='icontains')
    phone = CharFilter(field_name="phone", lookup_expr='icontains')

    il = CharFilter(field_name="il__name", lookup_expr='icontains')
    ilce = CharFilter(field_name="ilce__name", lookup_expr='icontains')
    mahallkoy = CharFilter(field_name="mahallekoy__name", lookup_expr='icontains')
    sokak = CharFilter(field_name="mahallekoy__name", lookup_expr='icontains')

    il_id = NumberFilter(field_name='il', lookup_expr='exact')
    ilce_id = NumberFilter(field_name='ilce', lookup_expr='exact')
    mahallekoy_id = NumberFilter(field_name='mahallekoy', lookup_expr='exact')
    sokak_id = NumberFilter(field_name='sokak', lookup_expr='exact')

    address = CharFilter(max_length=500, blank=True, null=True)
    code = CharFilter(max_length=4, blank=True, null=True, unique=True, verbose_name="Ofis Kodu")

    facebook = CharFilter(field_name="facebook", lookup_expr='icontains')
    twitter = CharFilter(field_name="twitter", lookup_expr='icontains')
    instagram = CharFilter(field_name="instagram", lookup_expr='icontains')
    tiktok = CharFilter(field_name="tiktok", lookup_expr='icontains')

    latitude = NumberFilter(field_name="latitude")
    longitude = NumberFilter(field_name="longitude")

    from_date = DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Ofis
        fields = []