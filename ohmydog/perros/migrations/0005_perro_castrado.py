# Generated by Django 4.2 on 2023-06-05 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perros', '0004_alter_perro_sexo'),
    ]

    operations = [
        migrations.AddField(
            model_name='perro',
            name='castrado',
            field=models.BooleanField(default=False),
        ),
    ]
