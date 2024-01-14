from abc import ABCMeta, abstractmethod

from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission, Group
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from attachment.serializers import AttachmentSerializer
from user.models import User


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['permissions'] = PermissionSerializer(obj.permissions, many=True).data
        return representation


class UserSerializerForSuperAdmin(serializers.ModelSerializer):
    broker = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id",
                  "broker",
                  "username",
                  "acente_temsilcisi",
                  "email",
                  "tckn",
                  "full_name",
                  "first_name",
                  "last_name",
                  "avatar",
                  "phone",
                  "role",
                  "date_joined",
                  "is_active",
                  "is_deleted",
                  "deleted_at",
                  "last_login"
                  )

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['avatar'] = AttachmentSerializer(obj.avatar).data if obj.avatar else None
        representation['acente_temsilcisi'] = UserSerializerForSuperAdmin(
            obj.acente_temsilcisi).data if obj.avatar else None
        return representation

    def get_broker(self, obj):
        from broker.models import Broker
        if Broker.objects.filter(user=obj).exists():
            from broker.serializers import BrokerForUserSerializer
            return BrokerForUserSerializer(obj.broker).data
        return None


class UserSerializer(serializers.ModelSerializer):
    broker = serializers.SerializerMethodField()
    provider = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id",
                  "broker",
                  "provider",
                  "avatar",
                  "acente_temsilcisi",
                  "first_name",
                  "last_name",
                  "tckn",
                  "email",
                  "phone",
                  "role",
                  "date_joined",
                  "is_active",
                  )

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['pk'] = obj.pk
        representation['avatar'] = AttachmentSerializer(obj.avatar).data if obj.avatar else None
        representation['acente_temsilcisi'] = UserSerializer(obj.acente_temsilcisi).data if obj.avatar else None

        return representation

    def get_provider(self, obj):
        from provider.models import Provider
        if Provider.objects.filter(user=obj).exists():
            from provider.serializers import ProviderForUserSerializer
            return ProviderForUserSerializer(Provider.objects.filter(user=obj).first()).data
        return None

    def get_broker(self, obj):
        from broker.models import Broker
        if Broker.objects.filter(user=obj).exists():
            from broker.serializers import BrokerForUserSerializer
            return BrokerForUserSerializer(Broker.objects.filter(user=obj).first()).data
        return None


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        return token

    def validate(self, attrs):
        # The default result (access/refresh tokens)
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for register user
    """
    role = serializers.CharField(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['role',
                  'first_name',
                  'last_name',
                  'email',
                  'phone',
                  'password']
        required = ['email', 'password']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.username = user.email
        user.save()
        return user

    def validate(self, data):
        if 'first_name' not in data:
            raise serializers.ValidationError(_("First Name is required!"))
        elif 'last_name' not in data:
            raise serializers.ValidationError(_("Last Name is required!"))
        elif 'email' not in data:
            raise serializers.ValidationError(_("Email is required!"))
        elif 'password' not in data:
            raise serializers.ValidationError(_("Password is required!"))
        elif 'phone' not in data:
            raise serializers.ValidationError(_("Password is required!"))

        return data

    def validate_email(self, email):
        """
        Check that the mail post is about Django.
        """
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("This email is already registered!"))
        elif '@' not in email or email == '':
            raise serializers.ValidationError(_("wrong email"))
        return email

    def validate_first_name(self, first_name):
        """
        Check that the mail post is about Django.
        """
        if first_name == '':
            raise serializers.ValidationError(_("FirstName cannot be empty!"))
        return first_name

    def validate_password(self, password):
        """
        Check that the mail post is about Django.
        """
        if len(password) < 6:
            raise serializers.ValidationError(_("Password must have at least 6 length!"))
        return password


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AttachmentSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "full_name", "email", "first_name", "last_name", "avatar", "phone", "role",
                  "date_joined", "groups", "user_permissions", "is_superuser", "is_staff")

    def create(self, validated_data):
        return super(ProfileSerializer, self).create(validated_data)

    def get_user_permissions(self, obj):
        pass


class UserPublicSerializer(serializers.ModelSerializer):
    avatar = AttachmentSerializer()
    broker = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id",
                  "broker",
                  "role",
                  "avatar",
                  "acente_temsilcisi",
                  "username",
                  "email",
                  "full_name",
                  "first_name",
                  "last_name",
                  "phone")

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['pk'] = obj.pk
        representation['avatar'] = AttachmentSerializer(obj.avatar).data if obj.avatar else None
        representation['acente_temsilcisi'] = UserSerializer(obj.acente_temsilcisi).data if obj.avatar else None

        return representation

    def get_broker(self, obj):
        from broker.models import Broker
        if Broker.objects.filter(user=obj).exists():
            from broker.serializers import BrokerForUserSerializer
            return BrokerForUserSerializer(obj.broker).data
        return None


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255)
    re_password = serializers.CharField(max_length=255)
    old_password = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ("id", "password", "re_password", "old_password")

    def validate(self, data):
        if data["password"] != data["re_password"]:
            raise serializers.ValidationError(_(f"Password and re_password are not matched"))
        return data


class PasswordDoneSerializer(serializers.Serializer):
    __metaclass__ = ABCMeta

    uid = serializers.CharField(max_length=255, required=True)
    token = serializers.CharField(max_length=255, required=True)
    new_password = serializers.CharField(max_length=20, required=True)

    @abstractmethod
    def validate(self, data):
        # Doing validation
        return data


class MyAuthTokenSerializer(serializers.Serializer):
    __metaclass__ = ABCMeta

    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password", ),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    @abstractmethod
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            # To authenticate call simply returns None for is_active=False users.
            # (Assuming the default ModelBackend authentication backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
