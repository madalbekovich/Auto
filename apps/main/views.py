from . import serializers, models
from rest_framework import generics

class StoriesView(generics.ListAPIView):
    queryset = models.Stories.objects.all()
    serializer_class = serializers.StoriesSerializer
