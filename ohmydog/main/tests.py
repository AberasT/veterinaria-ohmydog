from django.test import TestCase

# Create your tests here.
def es_veterinario(user):
    return user.is_staff

def es_superuser(user):
    return user.is_superuser

def es_cliente(user):
    return not user.is_staff
