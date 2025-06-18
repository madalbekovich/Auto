from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from . import serializers, models
from rest_framework import generics
from rest_framework import views

class VehicleTypeListView(generics.ListAPIView):
    """Тип автомобилей"""
    queryset = models.VehicleType.objects.all()
    serializer_class = serializers.VehicleTypeSerializer

class DealTypeListView(generics.ListAPIView):
    """Тип сделки"""
    queryset = models.DealType.objects.all()
    serializer_class = serializers.DealTypeSerializer

class CarMarkList(generics.ListAPIView):
    """Возвращает список марок"""
    queryset = models.CarMark.objects.all()
    serializer_class = serializers.CarMarkSerializer
    lookup_field = 'vehicle_type_id'

    def get_queryset(self):
        car_type = self.kwargs.get('vehicle_type_id')
        if car_type:
            return models.CarMark.objects.filter(id_car_type=car_type).select_related(
                'id_car_type'
            )
        return self.queryset.none()


class CarModeListView(generics.ListAPIView):
    """Модели автомобилей"""
    queryset = models.CarModel.objects.all()
    serializer_class = serializers.CarModelSerializer
    lookup_field = 'car_mark_id'

    def get_queryset(self):
        car_mark_id = self.kwargs.get('car_mark_id')
        if car_mark_id:
            return models.CarModel.objects.filter(id_car_mark=car_mark_id)
        return self.queryset.none()

class CarGenerationListView(generics.ListAPIView):
    """Поколения автомобилей"""
    queryset = models.CarGeneration.objects.all()
    serializer_class = serializers.CarGenerationSerializer
    lookup_field = 'car_model_id'

    def get_queryset(self):
        car_model_id = self.kwargs.get('car_model_id')
        if car_model_id:
            return models.CarGeneration.objects.filter(id_car_model=car_model_id)
        return self.queryset.none()

class CarTypeListView(generics.ListAPIView):
    """Тип автомобилей(седан, хэтчбек)"""
    queryset = models.CarType.objects.all()
    serializer_class = serializers.CarTypeSerializer

class PublicDataView(generics.GenericAPIView):
    def get(self, request):
        data = serializers.CombinedCarSerializer({
            "car_type": models.CarType.objects.only('id', 'name'),
            "fuel": models.Fuel.objects.only('id', 'name'),
            "transmission": models.Transmission.objects.only('id', 'name'),
            "gearbox_box": models.GearBox.objects.only('id', 'name'),
            "color": models.CarColor.objects.only('id', 'name'),
        }).data
        return Response(data, status=status.HTTP_200_OK)

class CarPostListView(generics.ListAPIView):
    """Возвращает список автомобилей на главной странице"""
    queryset = models.CarPost.objects.all()
    serializer_class = serializers.CarPostListSerializer

class MyAdsView(generics.ListAPIView):
    """Возвращает список объявлений пользователя"""
    permission_classes = [IsAuthenticated]
    queryset = models.CarPost.objects.all()
    serializer_class = serializers.CarPostListSerializer

    def get_queryset(self):
        user = self.request.user
        return models.CarPost.objects.filter(user=user)

class CarPostCreateView(generics.CreateAPIView):
    """Разместить объявление"""
    # permission_classes = [IsAuthenticated]
    queryset = models.CarPost.objects.all()
    serializer_class = serializers.CarPostCreateSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class CarPostUpdateView(generics.UpdateAPIView):
    """Изменить мои объявление"""
    permission_classes = [IsAuthenticated]
    queryset = models.CarPost.objects.all()
    serializer_class = serializers.CarPostCreateSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class MotorcycleCreateView(generics.CreateAPIView):
    """Разместить объявление мотоциклов"""
    permission_classes = [IsAuthenticated]
    queryset = models.CarPost.objects.all()
    serializer_class = serializers.MotorcycleCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SpecialCarCreateView(generics.CreateAPIView):
    """Разместить объявление спец.Техник"""
    permission_classes = [IsAuthenticated]
    queryset = models.CarPost.objects.all()
    serializer_class = serializers.SpecialCarCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CarFavoriteCreateView(views.APIView):
    """Добавить в избранное"""
    permission_classes = [IsAuthenticated]
    def post(self, request, car_id):
        try:
            car_post_instance = models.CarPost.objects.get(id=car_id)
            if car_post_instance:
                queryset = models.CarFavorite.objects.create(
                    user=request.user,
                    car_id=car_post_instance,
                )
                queryset.save()
                return Response({"response": True}, status=status.HTTP_200_OK)
        except Exception as _ex:
            return Response({"response": False}, status=status.HTTP_400_BAD_REQUEST)

class CarFavoriteListView(generics.ListAPIView):
    """Получить мои избранные авто"""
    queryset = models.CarPost.objects.all()
    serializer_class = serializers.CarPostListSerializer

    # def get_queryset(self):
    #     return models.CarFavorite.objects.filter(user=self.request.user)