# Generated by Django 4.1.2 on 2023-07-05 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0005_banka_toplam_bakiye_banka_toplam_cekilen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='banka',
            name='muh_kodu',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Muh Kodu'),
        ),
    ]
