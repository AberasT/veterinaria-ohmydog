# Generated by Django 4.2 on 2023-06-04 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0006_turno_cliente_alter_turno_perro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='hora',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
