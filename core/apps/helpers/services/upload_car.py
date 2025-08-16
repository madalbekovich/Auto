import requests
from django.core.files.base import ContentFile
import logging
from apps.cars.models import (
    Region, Currency, CarMark, CarModel, CarType, Fuel, Transmission, Condition,
    GearBox, SteeringWheel, CarGeneration, CarColor, Custom, CarPost, CarImage, DealType, VehicleType
)
from django.shortcuts import get_object_or_404
from apps.users.models import User


logger = logging.getLogger(__name__)

AUTO_AUTH = 'Bearer o0DfPm0UNcXwHFJpeKcNu8DxEGulHpUwuyXUvmVuDepb45tkTEjM8M42uryf9SAVqwXN1ct5C'
AUTH_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzIzODMzMTQsImV4cCI6MjA0Nzc0MzMxNCwidXNlcm5hbWUiOiI5OTY3MDkzNjIzNjAiLCJpcCI6IjE2Mi4xNTguMjIyLjE3MCIsImlkIjo5NjM3NzksInBob25lIjoiOTk2NzA5MzYyMzYwIiwibmFtZSI6IiJ9.PHKi7TMcBrQrtehXQjeeHE7-9iijStmiS6zjdQfd9qLC6gW1acClwmZDOWql-hz7osbXiESM2Yqma5gmvpmBBWULQQrvXawElHrYbXzpse04zPErd-IiX1xxgmIRmzIN_ylypcZyD9WMqkOyS0v_mAgymhObFMkj3HYtKPDlf2roxRLbUnngNLg46lTuJm-4mCN0XSCLMqoQM1uQ_r1udYmHEjOqsJY2ANZNcpiU0zSJ211Icug_JZgQiTL8MzWeAjGXgyU8VisvGCGXeS9ts2Onj7F58LDcqUNnZ6qT1_yvVqbUeZn2C5KHwx_dPqbraDkEI_eEJhM1SsDvbzR3MzJGW7kMdhfE9ELLFVFO7wpFherBN4HfmX4ubpeYIO5DCbrYwuAaCXSDLVuFF4vY9Ph6stknsn_ybU4XVDFASreX_c3AkGa3EeocVw1NyEDHfdTn3100esARUkhFj8ENYkc5ZX0TDotYhUCXwakSHcrjRLRO2wmAttT_hln9lt4A20e1U2JKGOj2Qf-XQYjEhQoFLiDd5dc7IQUB5lmEeZNk6FPGDhgBVht3fV_lm2sGFbUKxfPdR5ov7GT8Iyw8jz1v4q03HUCxp2__WjQgbMhG7kDub2ejSOg8tJkmSfxFVekcDqkwn1QzUopXYd4gNlmqAWAWVNa6V5XZjxc62EY'
headers = {'Authorization': f'Bearer {AUTH_KEY}', 'auto-auth': f'{AUTO_AUTH}'}


def upload_cars():
    URL = 'https://doubledragon.mashina.kg:443/v1/ads?filter=%7B%22type_id%22:[%7B%22value%22:%221%22,%22operator%22:%22=%22%7D]%7D&offset=0&limit=20&source=1&filter=%7B%22makes%22:[%7B%22id%22:116%7D]%7D&orderby=price&sort=desc'
    response = requests.get(URL, headers=headers)

    if response.status_code != 200:
        logger.error(f"Failed to fetch data from API: {response.status_code}")
        return

    data = response.json()
    datas = data.get('data', {})
    data_list = datas.get('list', [])

    for car_data in data_list:
        try:
            # Получение или создание связанных объектов
            region, _ = Region.objects.get_or_create(id=car_data.get('region', 1))
            currency, _ = Currency.objects.get_or_create(id=car_data.get('currency_id', 2))
            car_mark, _ = CarMark.objects.get_or_create(id=car_data.get('make', 176))
            deal_type, _ = DealType.objects.get_or_create(id=3)
            vehicle_type, _ = VehicleType.objects.get_or_create(id=1)
            car_model, _ = CarModel.objects.get_or_create(id=car_data.get('model', 1849),
                                                          defaults={'id_car_mark': car_mark})
            car_type, _ = CarType.objects.get_or_create(id=car_data.get('body', 15))  # Используем body вместо type_id
            fuel, _ = Fuel.objects.get_or_create(id=car_data.get('fuel', 1))
            transmission, _ = Transmission.objects.get_or_create(id=car_data.get('transmission', 3))
            condition, _ = Condition.objects.get_or_create(id=car_data.get('condition', 2))
            gearbox, _ = GearBox.objects.get_or_create(id=car_data.get('gear_box', 2))
            steering_wheel, _ = SteeringWheel.objects.get_or_create(id=car_data.get('steering_wheel', 1))
            car_generation, _ = CarGeneration.objects.get_or_create(id=car_data.get('generation_id', 6863),
                                                                    defaults={'id_car_model': car_model})
            color, _ = CarColor.objects.get_or_create(id=car_data.get('color', 3))
            custom, _ = Custom.objects.get_or_create(id=car_data.get('customs', 1))
            # year_car, _ = Year.objects.get_or_create(name=car_data.get('year', 2018))

            # Обработка пользователя
            try:
                user = User.objects.get(id=9)
            except User.DoesNotExist:
                user = User.objects.create(id=9, username='DefaultUser')

            # Обработка телефонов
            phones = car_data.get('phones', [])
            ctc_phone_1 = phones[0] if phones else car_data.get('phone', '+996')
            ctc_phone_2 = phones[1] if len(phones) > 1 else '+996'

            # Обработка цены (берём первую цену из списка prices)
            price = car_data.get('prices', [{}])[0].get('price', 0)

            # Создание или обновление записи CarPost
            car_post, created = CarPost.objects.update_or_create(
                unique_id=car_data.get('id'),
                defaults={
                    'user': user,
                    'deal_type': deal_type,
                    'region': region,
                    'currency': currency,
                    'vehicle_type': vehicle_type,
                    'car_brand': car_mark,
                    'car_model': car_model,
                    'car_type': car_type,
                    'fuel': fuel,
                    'transmission': transmission,
                    'gearbox': gearbox,
                    'steering_wheel': steering_wheel,
                    'car_generation': car_generation,
                    'color': color,
                    'condition': condition,
                    'custom': custom,
                    # 'year_car': year_car,
                    'mileage': car_data.get('mileage', 0),
                    'engine_volume': car_data.get('engine_volume', 0.0),
                    'description': car_data.get('description', ''),
                    'ctc_phone_1': ctc_phone_1,
                    'ctc_phone_2': ctc_phone_2,
                    'price': price,
                }
            )

            # Сохранение изображений (только ключ 'big')
            for image in car_data.get('images', []):
                image_url = image.get('big')
                if image_url:
                    save_image(image_url, car_post)

        except Exception as e:
            logger.error(f"Error processing car ID {car_data.get('id')}: {e}")


def save_image(image_url, car_post):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            filename = image_url.split('/')[-1]
            car_image = CarImage(car_post=car_post)
            car_image.img.save(filename, ContentFile(response.content), save=True)
            logger.info(f"Saved image {filename} for car {car_post.unique_id}")
        else:
            logger.error(f"Failed to fetch image: {image_url} (status code: {response.status_code})")
    except Exception as e:
        logger.error(f"Error saving image {image_url} for car {car_post.unique_id}: {e}")