from django.urls import path
from . import views

app_name = "cuidadores"
urlpatterns = [
    path("", views.index, name='index'),
]