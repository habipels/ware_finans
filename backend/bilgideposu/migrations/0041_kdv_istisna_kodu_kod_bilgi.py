# Generated by Django 4.1.2 on 2023-10-05 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0040_stok_kartlar_stok_birim_alis_satis_birimi'),
    ]

    operations = [
        migrations.AddField(
            model_name='kdv_istisna_kodu',
            name='kod_bilgi',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='KDV İstisna Kodu'),
        ),
    ]