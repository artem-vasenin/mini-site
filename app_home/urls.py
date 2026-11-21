from django.urls import path
from app_home import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='details'),
]