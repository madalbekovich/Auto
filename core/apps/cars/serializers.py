from rest_framework import serializers
from . import models
from drf_writable_nested import WritableNestedModelSerializer

from .models import SteeringWheel


class CarTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarType
        fields = "__all__"

class CarMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarMark
        fields = ['id', 'name', 'img']


"""
for mark in CarMark.objects.all():
    if mark.img and mark.img.name.startswith('media/'):
        mark.img.name = mark.img.name.replace('media/', '', 1)
        mark.save()
"""

class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarModel
        fields = "__all__"

class CarGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarGeneration
        fields = "__all__"

class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fuel
        fields = "__all__"

class TransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transmission
        fields = "__all__"

class GearBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GearBox
        fields = "__all__"

class CarColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarColor
        fields = "__all__"

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VehicleType
        fields = "__all__"

class DealTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DealType
        fields = "__all__"

class SteeringWheelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SteeringWheel
        fields = '__all__'

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Condition
        fields = '__all__'

class CarOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Condition
        fields = '__all__'

class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Custom
        fields = '__all__'

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Availability
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = '__all__'

class CombinedCarSerializer(serializers.Serializer):
    vehicle_type = VehicleTypeSerializer(many=True)
    deal_type = DealTypeSerializer(many=True)
    car_type = CarTypeSerializer(many=True)
    fuel = FuelSerializer(many=True)
    transmission = TransmissionSerializer(many=True)
    gearbox_box = GearBoxSerializer(many=True)
    color = CarColorSerializer(many=True)
    steering_wheel = SteeringWheelSerializer(many=True)
    condition = ConditionSerializer(many=True)
    count_owner = CarOwnerSerializer(many=True)
    custom = CustomSerializer(many=True)
    availability = AvailabilitySerializer(many=True)
    region = RegionSerializer(many=True)
    currency = CurrencySerializer(many=True)

# class CarImagePreviewSerializer(serializers.ModelSerializer):
#     preview_img = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = models.CarImage
#         fields = ['preview_img', ]
#
#     def get_preview_img(self, obj):
#         if obj.img:
#             return obj.img.url
#         return None

class CarPostListSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(read_only=True, source='region.name')
    mark_name = serializers.CharField(read_only=True, source='car_brand.name')
    model_name = serializers.CharField(read_only=True, source='car_model.name')
    currency = serializers.CharField(read_only=True, source='currency.sign')
    # preview_img = serializers.SerializerMethodField()
    class Meta:
        model = models.CarPost
        fields = ['id', 'preview_img', 'region_name', 'mark_name', 'model_name', 'short_description', 'price', 'currency']

    # def get_preview_img(self, obj):
    #     preview_img = obj.images.first()
    #     if preview_img:
    #         request = self.context.get('request')
    #         if request:
    #             return request.build_absolute_uri(preview_img.img.url)
    #     return None
class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarImage
        fields = ['img']

class CarPostCreateSerializer(WritableNestedModelSerializer):
    images = CarImageSerializer(many=True, write_only=True, required=False)
    class Meta:
        model = models.CarPost
        exclude = [
            'market_price_min',
            'market_price_max',
            'preview_img',
            'short_description',
            'user'
        ]

class MotorcycleCreateSerializer(WritableNestedModelSerializer):
    images = CarImageSerializer(many=True, write_only=True, required=False)
    class Meta:
        model = models.CarPost
        fields = [
            'user', 'vehicle_type', 'deal_type', 'images', 'car_brand',
            'year', 'price', 'currency', 'fuel', 'color', 'count_owner', 'condition',
            'availability', 'mileage', 'distance_unit', 'region', 'description'
        ]

class SpecialCarCreateSerializer(WritableNestedModelSerializer):
    images = CarImageSerializer(many=True, write_only=True, required=False)
    class Meta:
        model = models.CarPost
        fields = [
            'vehicle_type', 'deal_type', 'images', 'car_brand',
            'price', 'currency', 'fuel', 'color', 'condition',
            'region', 'description'
        ]

class CarFavoriteCreateSerializer(serializers.Serializer):
    car_id = serializers.IntegerField(required=True)

