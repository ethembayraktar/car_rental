from rest_framework import serializers

from country.models import Ilce, Il, MahalleKoy, CarMark, CarModel, Sokak, VehicleType


class IlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Il
        fields = ['id', 'name']


class IlceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ilce
        fields = ['id', 'il', 'name']


class MahalleKoySerializer(serializers.ModelSerializer):
    il_name = serializers.SerializerMethodField(read_only=True)
    ilce_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MahalleKoy
        fields = ['id', 'name', 'ilce', 'ilce_name', 'il_name', 'posta_kodu']

    def get_ilce_name(self, obj):
        return obj.ilce.name if obj.ilce else "No ilce"

    def get_il_name(self, obj):
        return obj.ilce.il.name if obj.ilce and obj.ilce.il else "il-ilce yok"


class SokakSerializer(serializers.ModelSerializer):
    il_name = serializers.SerializerMethodField(read_only=True)
    ilce_name = serializers.SerializerMethodField(read_only=True)
    mahallekoy_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Sokak
        fields = ['id', 'name', 'ilce', 'ilce_name', 'il_name', 'mahallekoy_name']

    def get_ilce_name(self, obj):
        return obj.ilce.name if obj.ilce else "No ilce"

    def get_il_name(self, obj):
        return obj.ilce.il.name if obj.ilce and obj.il else "il-ilce yok"

    def get_mahallekoy_name(self, obj):
        return obj.mahallekoy.name if obj.mahallekoy and obj.mahallekoy else "mahallekoy yok"


class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarMark
        fields = ['id', 'name', 'code']


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ['id', 'name', 'code', 'year', 'car_mark']

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['car_mark'] = CarMarkSerializer(obj.car_mark).data if obj.car_mark else None
        return representation


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'name']

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        return representation
