# Generated by Django 4.2 on 2023-06-12 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0018_alter_turno_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='hora',
            field=models.TimeField(blank=True, default='00:00', null=True),
        ),
    ]
