# Generated by Django 4.2 on 2023-07-10 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopcion', '0016_perroadopcion_activo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perroadopcion',
            name='raza',
            field=models.CharField(choices=[('mestizo', 'MESTIZO'), ('Siberian Husky', 'SIBERIAN HUSKY'), ('Beagle', 'BEAGLE'), ('Rottweiler', 'ROTTWEILER'), ('Bull Terrier', 'BULL TERRIER'), ('Bulldog Frances', 'BULLDOG FRANCES'), ('Boxer', 'BOXER'), ('Dogo Argentino', 'DOGO ARGENTINO'), ('Gran Danes', 'GRAN DANES'), ('Labrador', 'LABRADOR'), ('Galgo', 'GALGO'), ('Shiba Inu', 'SHIBA INU'), ('Akita Inu', 'AKITA INU'), ('Golden', 'GOLDEN'), ('Dalmata', 'DALMATA'), ('Chihuahua', 'CHIHUAHUA'), ('San Bernardo', 'SAN BERNARDO'), ('Doberman', 'DOBERMAN'), ('Pastor Aleman', 'PASTOR ALEMAN')], default='', max_length=20, null=True),
        ),
    ]
