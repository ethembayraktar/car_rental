from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from attachment.models import Attachment
from utils.constants import SUPER_ADMIN, ADMIN, EDITOR, CUSTOMER


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = _('Users')
        verbose_name = _('User')
        db_table = "user"
        ordering = ["pk"]

    ROLES = ((SUPER_ADMIN, "super_admin"),
             (ADMIN, "admin"),
             (EDITOR, "editor"),
             (CUSTOMER, "customer"),
             )

    username = models.CharField(_('username'), max_length=255, blank=True, null=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    full_name = models.CharField(max_length=550, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    tckn = models.CharField(max_length=11, default="00000000000", blank=True, null=True)
    kvvk_approval = models.BooleanField(default=False, blank=True, null=True)
    mss_approval = models.BooleanField(default=False, blank=True, null=True)
    cardUserKey = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone")
    avatar = models.ForeignKey(Attachment, max_length=255, blank=True, null=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=255, default=CUSTOMER, choices=ROLES)

    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False, blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)

    is_mobile_verified = models.BooleanField(default=False, blank=True, null=True)
    mobile_verified_at = models.DateTimeField(blank=True, null=True)

    guvenassist_sms_allowed = models.BooleanField(default=True, blank=True, null=True)
    guvenassist_email_allowed = models.BooleanField(default=True, blank=True, null=True)
    guvenassist_phone_allowed = models.BooleanField(default=True, blank=True, null=True)

    date_joined = models.DateTimeField(default=timezone.now, blank=True, null=True)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)
    deleted_by = models.ForeignKey('User', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name="user_deleted_by")
    deleted_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey('User', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name="user_created_by")

    acente_temsilcisi = models.ForeignKey('User', blank=True, null=True, on_delete=models.SET_NULL,
                                          related_name="user_agency_contact", verbose_name=_("Agency Contact"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def img_preview(self):  # new
        if self.avatar and self.avatar.webp:
            return mark_safe(f'<img src = "{self.avatar.webp.url}" width="100"/>')
        elif self.avatar and self.avatar.thumbnail:
            return mark_safe(f'<img src = "{self.avatar.thumbnail.url}" width="100"/>')
        elif self.avatar and self.avatar.original:
            return mark_safe(f'<img src = "{self.avatar.original.url}" width="100"/>')
        else:
            return None

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            self.full_name = "%s %s" % (self.first_name, self.last_name)
        else:
            self.full_name = ""
        is_new = self.id is None
        if is_new:
            self.username = self.email
            self.acente_temsilcisi = User.objects.filter(email="info@guvenassist.com").first()
        if self.is_superuser:
            self.role = SUPER_ADMIN

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email

