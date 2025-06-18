from django.db import models

class Stories(models.Model):
    img = models.ImageField("Оболожка истории", upload_to="car/stories/")
    link = models.URLField('Ссылка', max_length=500, blank=True, null=True, help_text='Если есть')
    created_at = models.DateTimeField("Дата и время", auto_now_add=True)

    class Meta:
        verbose_name = "Историю"
        verbose_name_plural = "Истории"

class StoriesImg(models.Model):
    stories_img = models.ForeignKey('Stories', on_delete=models.CASCADE, related_name='stories')
    description = models.TextField('Описание истории', null=True, blank=True)
    img = models.ImageField('Изображение истории', upload_to='car/stories/many_img')
    created_at = models.DateTimeField("Дата и время", auto_now_add=True)

    def __str__(self):
        return self.created_at.strftime("%d %B %Y г. %H:%M")