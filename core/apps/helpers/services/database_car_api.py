# import requests
# from apps.cars import models
#
# AUTH_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MzIzODMzMTQsImV4cCI6MjA0Nzc0MzMxNCwidXNlcm5hbWUiOiI5OTY3MDkzNjIzNjAiLCJpcCI6IjE2Mi4xNTguMjIyLjE3MCIsImlkIjo5NjM3NzksInBob25lIjoiOTk2NzA5MzYyMzYwIiwibmFtZSI6IiJ9.PHKi7TMcBrQrtehXQjeeHE7-9iijStmiS6zjdQfd9qLC6gW1acClwmZDOWql-hz7osbXiESM2Yqma5gmvpmBBWULQQrvXawElHrYbXzpse04zPErd-IiX1xxgmIRmzIN_ylypcZyD9WMqkOyS0v_mAgymhObFMkj3HYtKPDlf2roxRLbUnngNLg46lTuJm-4mCN0XSCLMqoQM1uQ_r1udYmHEjOqsJY2ANZNcpiU0zSJ211Icug_JZgQiTL8MzWeAjGXgyU8VisvGCGXeS9ts2Onj7F58LDcqUNnZ6qT1_yvVqbUeZn2C5KHwx_dPqbraDkEI_eEJhM1SsDvbzR3MzJGW7kMdhfE9ELLFVFO7wpFherBN4HfmX4ubpeYIO5DCbrYwuAaCXSDLVuFF4vY9Ph6stknsn_ybU4XVDFASreX_c3AkGa3EeocVw1NyEDHfdTn3100esARUkhFj8ENYkc5ZX0TDotYhUCXwakSHcrjRLRO2wmAttT_hln9lt4A20e1U2JKGOj2Qf-XQYjEhQoFLiDd5dc7IQUB5lmEeZNk6FPGDhgBVht3fV_lm2sGFbUKxfPdR5ov7GT8Iyw8jz1v4q03HUCxp2__WjQgbMhG7kDub2ejSOg8tJkmSfxFVekcDqkwn1QzUopXYd4gNlmqAWAWVNa6V5XZjxc62EY'
# AUTO_AUTH = 'Bearer o0DfPm0UNcXwHFJpeKcNu8DxEGulHpUwuyXUvmVuDepb45tkTEjM8M42uryf9SAVqwXN1ct5C'
# BASE_URL = 'https://doubledragon.mashina.kg:443/v1/public/data'
# headers = {'Authorization': f'Bearer {AUTH_KEY}', 'auto-auth': f'{AUTO_AUTH}'}
#
# def save_image(url, name):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(f'media/car/mark/mark_{name}.png', 'wb') as file:
#              file.write(response.content)
#         return f'media/car/mark/mark_{name}.png'
#     else:
#         return None
#         # raise Exception(f"Ошибка при скачивание изображение марки {url}")
#
# def upload_marks():
#     URL = 'https://doubledragon.mashina.kg:443/v1/public/data/'
#     response = requests.get(URL, headers=headers)
#
#     if response.status_code == 200:
#         print("Mark API\nOK..200")
#         data = response.json()
#
#         for data_list in data.get('data', {}).get('make', []):
#             instance_id = data_list.get('id')
#             instance_car_name = data_list.get('name')
#             logo = data_list.get('logo')
#             instance_car_type = models.CarType.objects.get(id=1)
#
#
#             instance_mark, created = models.CarMark.objects.get_or_create(
#                 id=instance_id,
#                 defaults={
#                     "name": instance_car_name,
#                     "id_car_type": instance_car_type,
#                     "img": save_image(logo, instance_car_name),
#                     "is_popular": bool(data_list.get('is_popular', 0))
#                 }
#             )
#
#             if created:
#                 print(f"Mark '{instance_car_name}' created successfully.")
#
#             for model_instance in data_list.get('models', []):
#                 id_model_instance = model_instance.get('id')
#                 name_model_instance = model_instance.get('name')
#                 is_popular = bool(model_instance.get('is_popular', 0))
#                 print(name_model_instance)
#                 car_model, created = models.CarModel.objects.update_or_create(
#                     id=id_model_instance,
#                     defaults={
#                         "name": name_model_instance,
#                         "is_popular": is_popular,
#                         "id_car_mark": instance_mark
#                     }
#                 )
#
#                 if created:
#                     print(f"Model '{name_model_instance}' created successfully for mark '{instance_mark.name}'.")
#
#     else:
#         print("STATUS CODE:", response.status_code)
#
# def upload_data():
#     response = requests.get(BASE_URL, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         data_list = data.get('data', {}).get('color', [])
#         for colors in data_list:
#             instance_name = colors.get('name', None)
#             instance_color = colors.get('color', 'Черный')
#             created = models.CarColor.objects.update_or_create(
#                 id=colors.get('id'),
#                 defaults={
#                     "name": instance_name,
#                     "color": instance_color,
#                 }
#             )
#             if created:
#                 print('Добавлено цвет:', instance_name)
#
#         data_list = data.get('data', []).get('fuel')
#         for fuel_data in data_list:
#             fuel, created = models.Fuel.objects.get_or_create(
#                 id=fuel_data.get('id'),
#                 defaults={
#                     "name": fuel_data.get('name'),
#                 })
#             if created:
#                 print('Добавлено trans: ', fuel)
#
#         gear_boxes = data.get('data', {}).get('gear_box', [])
#         for gear_box_data in gear_boxes:
#             gear_box_obj, created = models.GearBox.objects.update_or_create(
#                 id=gear_box_data.get('id'),
#                 defaults={
#                     "name": gear_box_data.get('name'),
#                 }
#             )
#             if created:
#                 print('Добавлена коробка передач: ', gear_box_obj)
#
#         steering_wheels = data.get('data', {}).get('steering_wheel', [])
#         for steering_wheels_data in steering_wheels:
#             steering_wheels_obj, created = models.SteeringWheel.objects.update_or_create(
#                 id=steering_wheels_data.get('id'),
#                 defaults={
#                     "name": steering_wheels_data.get('name'),
#                 }
#             )
#             if created:
#                 print('Добавлена коробка Руль управления: ', steering_wheels_obj)
#
#         car_condition = data.get('data', {}).get('car_condition', [])
#         for car_condition_data in car_condition:
#             car_condition_obj, created = models.Condition.objects.update_or_create(
#                 id=car_condition_data.get('id'),
#                 defaults={
#                     "name": car_condition_data.get('name'),
#                 }
#             )
#             if created:
#                 print('Добавлена car_condition: ', car_condition_obj)
#
#         transmission = data.get('data', {}).get('transmission', [])
#         for transmission_data in transmission:
#             transmission_obj, created = models.Transmission.objects.update_or_create(
#                 id=transmission_data.get('id'),
#                 defaults={
#                     "name": transmission_data.get('name'),
#                 }
#             )
#             if created:
#                 print('Добавлена transmission: ', transmission_obj)
#
#         currency = data.get('data', {}).get('currency', [])
#         for currency_data in currency:
#             currency_obj, created = models.Currency.objects.update_or_create(
#                 id=currency_data.get('id'),
#                 defaults={
#                     "name": currency_data.get('name'),
#                     "sign": currency_data.get('sign'),
#                     "is_default": bool(currency_data.get('is_default', 0))
#                 }
#             )
#             if created:
#                 print('Добавлена currency: ', currency_obj)
#         # exterior = data.get('data', {}).get('exterior', [])
#         # for exterior_data in exterior:
#         #     exterior_obj, created = Exterior.objects.update_or_create(
#         #         id=exterior_data.get('id'),
#         #         defaults={
#         #             "name": exterior_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена exterior: ', exterior_obj)
#
#         # interior = data.get('data', {}).get('interior', [])
#         # for interior_data in interior:
#         #     interior_obj, created = Interior.objects.update_or_create(
#         #         id=interior_data.get('id'),
#         #         defaults={
#         #             "name": interior_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена interior: ', interior_obj)
#
#         # media = data.get('data', {}).get('media', [])
#         # for media_data in media:
#         #     media_obj, created = Media.objects.update_or_create(
#         #         id=media_data.get('id'),
#         #         defaults={
#         #             "name": media_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена media: ', media_obj)
#
#         # media = data.get('data', {}).get('media', [])
#         # for media_data in media:
#         #     media_obj, created = Media.objects.update_or_create(
#         #         id=media_data.get('id'),
#         #         defaults={
#         #             "name": media_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена media: ', media_obj)
#
#         # safety = data.get('data', {}).get('safety', [])
#         # for safety_data in safety:
#         #     safety_obj, created = Safety.objects.update_or_create(
#         #         id=safety_data.get('id'),
#         #         defaults={
#         #             "name": safety_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена safety: ', safety_obj)
#         #
#         # other_options = data.get('data', {}).get('other_option', [])
#         # for other_options_data in other_options:
#         #     other_options_obj, created = OtherOptions.objects.update_or_create(
#         #         id=other_options_data.get('id'),
#         #         defaults={
#         #             "name": other_options_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена other_options: ', other_options_obj)
#         #
#         # configuration = data.get('data', {}).get('configuration', [])
#         # for configuration_data in configuration:
#         #     configuration_obj, created = GeneralOptions.objects.update_or_create(
#         #         id=configuration_data.get('id'),
#         #         defaults={
#         #             "name": configuration_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена configuration: ', configuration_obj)
#
#         # featured_option = data.get('data', {}).get('featured_option', [])
#         # for featured_option_data in featured_option:
#         #     featured_option_obj, created = FeaturedOption.objects.update_or_create(
#         #         id=featured_option_data.get('id'),
#         #         defaults={
#         #             "name": featured_option_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена featured_option: ', featured_option_obj)
#         #
#         # registration_country = data.get('data', {}).get('registration_country', [])
#         # for registration_country_data in registration_country:
#         #     registration_country_obj, created = RegistrationCountry.objects.update_or_create(
#         #         id=registration_country_data.get('id'),
#         #         defaults={
#         #             "name": registration_country_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена registration_country: ', registration_country_obj)
#
#         # comment_allowed = data.get('data', {}).get('comment_allowed', [])
#         # for comment_allowed_data in comment_allowed:
#         #     comment_allowed_obj, created = CommentAllowed.objects.update_or_create(
#         #         id=comment_allowed_data.get('id'),
#         #         defaults={
#         #             "name": comment_allowed_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена comment_allowed: ', comment_allowed_obj)
#
#         # exchange = data.get('data', {}).get('exchange', [])
#         # for exchange_data in exchange:
#         #     exchange_obj, created = Exchange.objects.update_or_create(
#         #         id=exchange_data.get('id'),
#         #         defaults={
#         #             "name": exchange_data.get('name'),
#         #         }
#         #     )
#         #     if created:
#         #         print('Добавлена exchange: ', exchange_obj)
#
#     else:
#         print(response.status_code)
#
#
# def test_json():
#     URL = 'https://doubledragon.mashina.kg:443/v1/public/data'
#
#     headers = {
#         'Authorization': f'Bearer {AUTH_KEY}',
#         'auto-auth': f'{AUTO_AUTH}'
#     }
#     response = requests.get(URL, headers=headers)
#
#     if response.status_code == 200:
#         return 200
#     else:
#         return 500
#
# if __name__ == "__main__":
#     status_test = test_json()
#     if status_test == 200:
#         upload_marks()
#         upload_data()
#     else:
#         print('error when fetching data')


import  requests

URL = 'http://auto-park.online/car/public-data/'
response = requests.get(URL)

if response.status_code == 200:
    print(response.json())
else:
    print('not')