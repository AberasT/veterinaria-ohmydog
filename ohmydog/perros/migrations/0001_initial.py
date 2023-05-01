# Generated by Django 4.2 on 2023-05-01 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='-', max_length=20, null=True)),
                ('color', models.CharField(default='-', max_length=20, null=True)),
                ('raza', models.CharField(blank=True, default='-', max_length=20, null=True)),
                ('sexo', models.CharField(choices=[('MACHO', 'M'), ('HEMBRA', 'H'), ('-', 'Ns')], default='-', max_length=6)),
                ('fecha_nacimiento', models.DateField()),
                ('peso', models.CharField(blank=True, default='-', max_length=5, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_perros', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
