from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from . import models
# from core.settings import BASE_URL
from django.conf import settings
import random

@receiver(post_save, sender=models.CarImage)
def update_preview_image(sender, instance, **kwargs):
    """Денормализация сохраняем урл первого изображения в preview_img"""
    car_post = instance.car_post
    first_image = car_post.images.first()

    new_preview_img = first_image.img.url if first_image else 'https://example.com'

    if car_post.preview_img != new_preview_img:
        car_post.preview_img = f"{settings.BASE_URL}{new_preview_img}"
        post_save.disconnect(update_preview_image, sender=models.CarImage)
        car_post.save(update_fields=['preview_img'])
        post_save.connect(update_preview_image, sender=models.CarImage)

@receiver(post_delete, sender=models.CarImage)
def update_preview_image_on_delete(sender, instance, **kwargs):
    """Обновляем preview_img при удалении изображения."""
    car_post = instance.car_post
    first_image = car_post.images.first()

    new_preview_img = first_image.img.url if first_image else 'https://example.com'

    if car_post.preview_img != new_preview_img:
        car_post.preview_img = f"{settings.BASE_URL}{new_preview_img}"
        post_save.disconnect(update_preview_image, sender=models.CarImage)
        car_post.save(update_fields=['preview_img'])
        post_save.connect(update_preview_image, sender=models.CarImage)

@receiver(post_save, sender=models.CarPost)
def update_short_description(sender, instance, **kwargs):
    """Автоматически создает краткое описание из description"""
    car_description = instance.description
    new_short_description = f"{car_description[:30]}.." if car_description else ""

    if instance.short_description != new_short_description:
        instance.short_description = new_short_description
        post_save.disconnect(update_short_description, sender=models.CarPost)
        instance.save(update_fields=['short_description'])
        post_save.connect(update_short_description, sender=models.CarPost)

@receiver(post_save, sender=models.CarPost)
def set_unique_id_car(sender, instance, created, **kwargs):
    if created:
        car_number = random.randint(9219_0000, 9999_9999)
        instance.unique_id = car_number
        instance.save(update_fields=['unique_id'])
