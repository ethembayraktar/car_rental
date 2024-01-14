from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import EmailField, CharField
from django.utils.translation import gettext_lazy as _

from user.models import User


class UserCreationFormExtended(UserCreationForm):
    first_name = forms.CharField(
        label=_("First Name"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ("username", "email", "last_name", "password")

        field_classes = {"username": UsernameField, "email": EmailField, "first_name": CharField,
                         "last_name": CharField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Type in username"
        self.fields["email"].widget.attrs["placeholder"] = "Type in email"
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"


class UserAdminConfig(UserAdmin):
    list_display = (
        'email', 'username', 'img_preview', 'role', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser',
        'last_login')
    search_fields = ('id', 'first_name', 'last_name', 'email')

    model = User
    ordering = ('-date_joined',)
    fieldsets = (
        (_("Account info"), {"fields": ("username", "email", "password")}),
        (
            _("Personal info"), {
                "fields": (
                    "avatar",
                    "first_name",
                    "last_name",
                    "tckn",
                    "role",
                    "phone")}),
        (
            _("Permissions"),
            {
                "fields": (

                    "kvvk_approval",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_email_verified",
                    "is_mobile_verified",
                    "is_deleted",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important People"), {
                "fields": (
                    "acente_temsilcisi",
                    "deleted_by",
                    "created_by")}),
        (
            _("Important dates"),
            {
                "fields": (
                    "email_verified_at",
                    "mobile_verified_at",
                    "deleted_at",
                    "last_login",
                    "date_joined"
                )}),

    )


admin.site.register(User, UserAdminConfig)
