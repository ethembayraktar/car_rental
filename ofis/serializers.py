from rest_framework import serializers

from attachment.serializers import AttachmentSerializer
from ofis.models import Ofis


class OfisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ofis
        fields = ("id",
                  "code",
                  "user",
                  "logo",
                  "name",
                  "email",
                  "phone",
                  "il",
                  "ilce",
                  "mahallekoy",
                  "sokak",
                  "address",
                  "facebook",
                  "twitter",
                  "instagram",
                  "tiktok",
                  "latitude",
                  "longitude"
                  )

    def to_representation(self, obj):
        from user.serializers import UserPublicSerializer
        representation = super().to_representation(obj)
        representation['logo'] = AttachmentSerializer(obj.logo).data if obj.logo else None
        representation['user'] = UserPublicSerializer(obj.user).data if obj.user else None
        return representation
