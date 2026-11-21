from django.urls import path
from app_weight import views


app_name = 'weight'

urlpatterns = [
    path('', views.index, name='details'),
    path('create/', views.create, name='create'),
    path('file/', views.file, name='file'),
    path('edit/<int:pk>', views.edit, name='edit'),
    path('delete/<int:pk>', views.delete, name='delete'),
]