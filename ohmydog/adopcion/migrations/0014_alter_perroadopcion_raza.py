# Generated by Django 4.2 on 2023-06-12 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopcion', '0013_alter_perroadopcion_fecha_adopcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perroadopcion',
            name='raza',
            field=models.CharField(choices=[('mestizo', 'MESTIZO'), ('Siberian Husky', 'SIBERIAN HUSKY'), ('Beagle', 'BEAGLE'), ('Rottweiler', 'ROTTWEILER'), ('Bull Terrier', 'BULL TERRIER'), ('Bulldog Frances', 'BULLDOG FRANCES'), ('Boxer', 'BOXER'), ('Dogo Argentino', 'DOGO ARGENTINO'), ('Gran Danes', 'GRAN DANES'), ('Labrador', 'LABRADOR'), ('Galgo', 'GALGO'), ('Shiba Inu', 'AKITA INU'), ('Golden', 'GOLDEN'), ('Dalmata', 'DALMATA'), ('Chihuahua', 'CHIHUAHUA'), ('San Bernardo', 'SAN BERNARDO'), ('Doberman', 'DOBERMAN')], default='', max_length=20, null=True),
        ),
    ]
