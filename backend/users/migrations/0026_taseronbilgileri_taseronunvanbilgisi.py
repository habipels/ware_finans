# Generated by Django 4.1.2 on 2023-09-24 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_kurumlar_dar_mukkelef_kimlik_ve_adres_bilgisi'),
    ]

    operations = [
        migrations.AddField(
            model_name='taseronbilgileri',
            name='taseronunvanbilgisi',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Taşeron Unvan Bilgisi'),
        ),
    ]