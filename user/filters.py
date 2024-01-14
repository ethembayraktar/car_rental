import django_filters
from django_filters import CharFilter, BooleanFilter

from user.models import User


class UserFilter(django_filters.FilterSet):
    role = CharFilter(field_name='role', lookup_expr='icontains')
    email = CharFilter(field_name='email', lookup_expr='icontains')

    is_active = BooleanFilter(field_name='is_active')
    is_staff = BooleanFilter(field_name='is_staff')
    is_mobile_verified = BooleanFilter(field_name='is_mobile_verified')
    guvenassist_sms_allowed = BooleanFilter(field_name='guvenassist_sms_allowed')
    guvenassist_email_allowed = BooleanFilter(field_name='guvenassist_email_allowed')
    guvenassist_phone_allowed = BooleanFilter(field_name='guvenassist_phone_allowed')

    from_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = User
        fields = []
