# Generated by Django 4.2 on 2023-05-30 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopcion', '0007_alter_perroadopcion_fecha_adopcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perroadopcion',
            name='fecha_adopcion',
            field=models.DateField(null=True),
        ),
    ]
