from abc import ABCMeta, abstractmethod

from rest_framework import serializers

from attachment.serializers import AttachmentSerializer
from frontend.models import Frontend, Seo
from kampanya.models import Kampanya


class KampanyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kampanya
        fields = ("id",
                  "title",
                  "slug",
                  "summary",
                  "details",
                  "order",
                  "started_at",
                  "end_at",
                  "created_at",
                  "updated_at",
                  "created_by",
                  "updated_by",

                  )

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['banner'] = AttachmentSerializer(obj.banner,
                                                        context=self.context).data if obj.banner else None

        return representation
