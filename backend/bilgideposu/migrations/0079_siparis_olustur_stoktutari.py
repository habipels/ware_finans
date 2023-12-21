# Generated by Django 4.1.2 on 2023-10-31 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0078_stok_birim_alis_satis_birimi_stokmiktari'),
    ]

    operations = [
        migrations.AddField(
            model_name='siparis_olustur',
            name='stoktutari',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Stok Tutarı TL'),
        ),
    ]