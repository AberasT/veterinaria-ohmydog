from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = ["dni", "nombre", "apellido", "email"]