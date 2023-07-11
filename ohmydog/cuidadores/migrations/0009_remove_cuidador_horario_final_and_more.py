# Generated by Django 4.2 on 2023-07-11 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cuidadores', '0008_solicitud_apellido_solicitud_email_solicitud_nombre_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuidador',
            name='horario_final',
        ),
        migrations.RemoveField(
            model_name='cuidador',
            name='horario_inicial',
        ),
        migrations.AddField(
            model_name='cuidador',
            name='disponibilidad',
            field=models.CharField(default='', max_length=500, null=True),
        ),
    ]
