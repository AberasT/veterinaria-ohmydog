from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.loginView, name='login'),
    path("logout/", views.logoutView, name='logout'),
]