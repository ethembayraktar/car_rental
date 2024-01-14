from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CountryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'country'
    verbose_name = _("Country")
