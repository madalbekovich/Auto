from django.contrib import admin
from . import models

class StoryModelAdmin(admin.StackedInline):
    model = models.StoriesImg
    extra = 1
    def render_image(self, obj):
        if obj:
            return obj.description
        return 'no'

@admin.register(models.Stories)
class StoriesModelAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = [StoryModelAdmin]


