from django.urls import path
from app_weight import views


app_name = 'weight'

urlpatterns = [
    path('', views.index, name='details'),
]