# Generated by Django 4.1.2 on 2024-01-04 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0105_musavir_stok'),
    ]

    operations = [
        migrations.AddField(
            model_name='musavir_stok',
            name='stok_kodu',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Stok Kodu'),
        ),
    ]
