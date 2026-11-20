from django.urls import path
from app_weight import views


urlpatterns = [
    path('', views.index),
]