# Generated by Django 4.1.2 on 2023-12-21 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0101_tevkifat_tur_kodu_aciklama_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hesapplanlari',
            name='kdv_orani',
            field=models.FloatField(default=0, verbose_name='KDV Oranı'),
        ),
    ]