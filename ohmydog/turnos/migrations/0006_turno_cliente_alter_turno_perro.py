# Generated by Django 4.2 on 2023-06-03 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('turnos', '0005_remove_turno_cliente_alter_turno_hora_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='turno',
            name='cliente',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='usuarios_turnos', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='turno',
            name='perro',
            field=models.CharField(max_length=30),
        ),
    ]
