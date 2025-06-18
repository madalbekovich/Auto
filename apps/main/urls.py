from . import views
from django.urls import path

urlpatterns = [
    path('stories/', views.StoriesView.as_view())
]