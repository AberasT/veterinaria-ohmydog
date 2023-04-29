from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name='index'),
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    # path("error/", views.error, name='error')
]