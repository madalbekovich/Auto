from rest_framework import serializers
from . import models

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoriesImg
        fields = '__all__'

class StoriesSerializer(serializers.ModelSerializer):
    stories = StorySerializer(many=True)
    class Meta:
        model = models.Stories
        fields = '__all__'
