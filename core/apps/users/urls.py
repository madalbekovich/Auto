from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.SendCodeView.as_view()),
    path('verify-login/', views.VerifyPhoneView.as_view()),
    path('update/', views.UserUpdateView.as_view()),
]