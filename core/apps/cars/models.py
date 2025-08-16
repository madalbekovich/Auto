from . import choices
from django.db import models
from apps.users.models import User

class CarType(models.Model):
    name = models.CharField('Тип кузова', max_length=100)
    img = models.ImageField('Фото типа машины', upload_to='car/car_type/', null=True, blank=True)

    def __str__(self):
        return self.name

class DealType(models.Model):
    name = models.CharField('Тип сделки', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип предложений'
        verbose_name_plural = 'Тип предложения'

class VehicleType(models.Model):
    name = models.CharField('Тип Автомобиля', max_length=100)

    class Meta:
        verbose_name = 'Тип автомобиля'
        verbose_name_plural = 'Тип автомобилей'

class CarMark(models.Model):
    id_car_type = models.ForeignKey('CarType', on_delete=models.CASCADE)
    name = models.CharField('Название марки', max_length=100)
    img = models.ImageField('Фото автомобиля', upload_to='car/mark/', null=True, blank=True)
    is_popular = models.BooleanField(default=False, verbose_name='Популярная марка')

    def __str__(self):
        return self.name

class CarModel(models.Model):
    id_car_mark = models.ForeignKey("CarMark", on_delete=models.CASCADE, related_name="car_mark")
    name = models.CharField("Название модели", max_length=100)
    is_popular = models.BooleanField(default=False, verbose_name='Популярная модель')

    def __str__(self):
        return f"{self.name}"

class CarGeneration(models.Model):
    id_car_model = models.ForeignKey("CarModel", on_delete=models.CASCADE)
    year_begin = models.CharField("Начало выпуска от", null=True, max_length=255)
    year_end = models.CharField("Год выпуска до", null=True, max_length=255)
    seria = models.CharField('Серия', max_length=255)
    img = models.ImageField('Фото поколение', null=True, blank=True, upload_to='car/generation/')

    def __str__(self):
        return f"{self.id} - {self.id_car_model.id_car_mark.name} - {self.id_car_model.name}"

class Transmission(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Fuel(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class GearBox(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class SteeringWheel(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class CarColor(models.Model):
    name = models.CharField("Название", max_length=300, null=True)
    color = models.CharField("Цвет", max_length=300, null=True)
    def __str__(self):
        return self.name

class CarOwner(models.Model):
    name = models.CharField("Владелец", max_length=300, null=True)
    def __str__(self):
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Custom(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Availability(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=50)
    sign = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CarPost(models.Model):
    """Модель для объявление автомобилей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    unique_id = models.IntegerField(verbose_name='Уникальный идентификатор машины', null=True, blank=True)

    vehicle_type = models.ForeignKey('VehicleType', on_delete=models.CASCADE, verbose_name='Тип автомобиля')
    deal_type = models.ForeignKey('DealType', on_delete=models.CASCADE, verbose_name='Тип расчета')

    car_type = models.ForeignKey('CarType', on_delete=models.CASCADE, verbose_name='Тип кузова', null=True, blank=True)
    car_brand = models.ForeignKey('CarMark', on_delete=models.CASCADE, verbose_name='Марка', null=True, blank=True)
    car_model = models.ForeignKey('CarModel', on_delete=models.CASCADE, verbose_name='Модель', null=True, blank=True)
    car_generation = models.ForeignKey('CarGeneration', on_delete=models.CASCADE, verbose_name='Поколение', null=True, blank=True)

    fuel = models.ForeignKey('Fuel', on_delete=models.CASCADE, verbose_name='Тип двигателя', null=True, blank=True)
    transmission = models.ForeignKey('Transmission', on_delete=models.CASCADE, verbose_name='Привод', null=True, blank=True)
    gearbox = models.ForeignKey('Gearbox', on_delete=models.CASCADE, verbose_name='Коробка передач', null=True, blank=True)
    color = models.ForeignKey('CarColor', on_delete=models.CASCADE, verbose_name='Цвет')
    count_owner = models.ForeignKey('CarOwner', on_delete=models.CASCADE, verbose_name='К-лво Владелец', null=True, blank=True)
    steering_wheel = models.ForeignKey('SteeringWheel', on_delete=models.CASCADE, verbose_name='Руль', null=True, blank=True)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE, verbose_name='Техническое состояние', null=True, blank=True)
    custom = models.ForeignKey('Custom', on_delete=models.CASCADE, verbose_name='Расстоможен', null=True, blank=True)
    availability = models.ForeignKey('Availability', on_delete=models.CASCADE, verbose_name='Наличии', null=True, blank=True)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='Регион продажи')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='Валюта цены')

    year = models.IntegerField(default=1900, verbose_name='Год выпуска', null=True, blank=True)
    engine_volume = models.FloatField(verbose_name='Объем двигателя (л)', null=True, blank=True)

    mileage = models.IntegerField(default=000000, verbose_name='Пробег')
    distance_unit = models.CharField(choices=choices.DISTANCE_UNIT_CHOICES, default='KM', verbose_name='Измерения расстояния', max_length=10)
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='Цена')
    # currency = models.CharField(default='Сом', choices=choices.CURRENCY, verbose_name='Валюта цены')

    vin_code = models.CharField(default='01KG000ABC', verbose_name='VIN код', max_length=10)
    description = models.TextField(verbose_name='Дополнительная информация')
    short_description = models.TextField(null=True, blank=True, verbose_name='Краткая информация', editable=True)
    ctc_phone_1 = models.CharField(default='+996', max_length=50, verbose_name='Телефонный номер для контакта1')
    ctc_phone_2 = models.CharField(default='+996', max_length=50, verbose_name='Телефонный номер для контакта2')

    market_price_min = models.CharField(default=0, verbose_name='Анализ рынка цена от', max_length=20)
    market_price_max = models.CharField(default=0, verbose_name='Анализ рынка цена до', max_length=20)
    preview_img = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.description
    # def save(self, *args, **kwargs):
    #     if self.description:
    #         self.short_description = f"{self.description[:30]}.."
    #     else:
    #         self.short_description = ''
    #     super().save(*args, **kwargs)


class CarImage(models.Model):
    car_post = models.ForeignKey('CarPost', on_delete=models.CASCADE, verbose_name='Картинки автомобиля', related_name='images')
    img = models.ImageField(upload_to='car/posts/')

    class Meta:
        verbose_name = 'Картинки автомобиля'
        verbose_name_plural = 'Картинки автомобиля'

class CarFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_id = models.ForeignKey('CarPost', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время добавление в избранное')

    class Meta:
        unique_together = ['car_id']
