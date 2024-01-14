import logging

from rest_framework import serializers

from attachment.models import Attachment
from core.settings import ROOT


class AttachmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'slug', 'thumbnail', 'original', 'webp', 'title']

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['original'] = f"{ROOT}{obj.original.url}" if obj.original else None
        representation['thumbnail'] = f"{ROOT}{obj.thumbnail.url}" if obj.thumbnail else None
        representation['webp'] = f"{ROOT}{obj.webp.url}" if obj.webp else None
        return representation

    def validate_original(self, original):
        if isinstance(original, str):
            return None
        return original

    def create(self, validated_data):
        try:
            return super(AttachmentCreateSerializer, self).create(validated_data)
        except Exception as e:
            logging.exception(e)
            print(e)
            return None


class AttachmentSerializer(serializers.ModelSerializer):
    original = serializers.CharField()
    thumbnail = serializers.CharField()
    webp = serializers.CharField()
    id = serializers.IntegerField()

    class Meta:
        model = Attachment
        fields = ['id',
                  'thumbnail',
                  'original',
                  'webp',
                  'title',
                  'mime',
                  ]

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['pk'] = obj.id
        representation['original'] = f"{ROOT}{obj.original.url}" if obj.original else None
        representation['thumbnail'] = f"{ROOT}{obj.thumbnail.url}" if obj.thumbnail else None
        representation['webp'] = f"{ROOT}{obj.webp.url}" if obj.webp else None
        return representation
