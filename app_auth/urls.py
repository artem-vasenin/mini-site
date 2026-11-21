from django.urls import path
from django.contrib.auth.views import LogoutView
from app_auth import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path("logout/", LogoutView.as_view(next_page="home:details"), name="logout"),
]