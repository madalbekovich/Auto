from django.urls import path
from . import views

urlpatterns = [
    path('public-data/', views.PublicDataView.as_view()),
    path('ads/', views.CarPostListView.as_view()),
    path('ads-update/<int:id>', views.CarPostUpdateView.as_view()),
    path('deploy-car/', views.CarPostCreateView.as_view()),
    path('deploy-motorcycle/', views.MotorcycleCreateView.as_view()),
    path('deploy-special-car/', views.SpecialCarCreateView.as_view()),
    path('my-ads/', views.MyAdsView.as_view()),
    path('set-favorite/<int:car_id>', views.CarFavoriteCreateView.as_view()),
    path('my-favorite/', views.CarFavoriteListView.as_view()),

    # Данные авто

    path('vehicle/', views.VehicleTypeListView.as_view()),
    path('deal-type/', views.DealTypeListView.as_view()),
    path('mark/<int:vehicle_type_id>', views.CarMarkList.as_view()),
    path('model/<int:car_mark_id>', views.CarModeListView.as_view()),
    path('generation/<int:car_model_id>', views.CarGenerationListView.as_view()),
    path('type/', views.CarTypeListView.as_view()),
]