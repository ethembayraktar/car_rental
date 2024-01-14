from abc import ABCMeta, abstractmethod

from rest_framework import serializers

from attachment.serializers import AttachmentSerializer
from frontend.models import Frontend, Seo


class FrontendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frontend
        fields = ("id",
                  "site_name",
                  "address",
                  "panel_login_bg",
                  "ajax_loading",
                  "logo",
                  "favicon",
                  "phone1",
                  "phone2",
                  "email1",
                  "email2",
                  'is_active',
                  'is_deleted',
                  'slug',
                  'title',
                  'sub_title',
                  'short_text',
                  'text',
                  'contact_image',
                  'footer_image',
                  'image1',
                  'image2',
                  'image_add_video',
                  'add_video',
                  "linkedin",
                  "instagram",
                  "youtube",
                  "facebook",
                  "tiktok",
                  "twitter",
                  )

    def to_representation(self, obj):
        representation = super().to_representation(obj)

        representation["text"] = obj.text if obj.text else None
        representation["short_text"] = obj.short_text if obj.short_text else None
        representation['ajax_loading'] = AttachmentSerializer(obj.ajax_loading,
                                                              context=self.context).data if obj.ajax_loading else None
        representation['panel_login_bg'] = AttachmentSerializer(obj.panel_login_bg,
                                                                context=self.context).data if obj.panel_login_bg else None

        representation['logo'] = AttachmentSerializer(obj.logo,
                                                      context=self.context).data if obj.logo else None
        representation['favicon'] = AttachmentSerializer(obj.favicon,
                                                         context=self.context).data if obj.favicon else None
        representation['footer_image'] = AttachmentSerializer(obj.footer_image,
                                                              context=self.context).data if obj.footer_image else None
        representation['image1'] = AttachmentSerializer(obj.image1,
                                                        context=self.context).data if obj.image1 else None
        representation['image2'] = AttachmentSerializer(obj.image2,
                                                        context=self.context).data if obj.image2 else None


        return representation


class SeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seo
        fields = "__all__"

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        return representation


class UploadSerializer(serializers.Serializer):
    __metaclass__ = ABCMeta

    file_uploaded = serializers.FileField()

    class Meta:
        fields = ('file_uploaded',)

    @abstractmethod
    def validate(self, data):
        # Doing validation
        return data


# Serializer for multiple files upload.
class MultipleFilesUploadSerializer(serializers.Serializer):
    __metaclass__ = ABCMeta

    file_uploaded = serializers.ListField()

    class Meta:
        fields = ('file_uploaded',)

    @abstractmethod
    def validate(self, data):
        # Doing validation
        return data
