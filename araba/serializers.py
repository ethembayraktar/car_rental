from rest_framework import serializers

from araba.models import Araba, CarModel, VehicleType, CarMark
from ofis.serializers import OfisSerializer


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


class ArabaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Araba
        fields = ["name",
                  "ofis",
                  "vehicle_plate",
                  "vehicle_register_seri",
                  "vehicle_register_no",
                  "vehicle_type",
                  "car_mark",
                  "car_model",
                  "car_model_year",
                  "transmission",
                  "fuel",
                  "deposit",
                  "mileage",
                  "age",
                  "cost_of_rental",
                  "km_min_constraint",
                  "age_min_constraint",
                  "licence_min_constraint",
                  "payment_constraint"
                  ]

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['car_mark'] = CarMarkSerializer(obj.car_mark).data if obj.car_mark else None
        representation['car_model'] = CarModelSerializer(obj.car_model).data if obj.car_model else None
        representation['vehicle_type'] = VehicleTypeSerializer(obj.vehicle_type).data if obj.vehicle_type else None
        representation['ofis'] = OfisSerializer(obj.ofis).data if obj.ofis else None
        return representation
