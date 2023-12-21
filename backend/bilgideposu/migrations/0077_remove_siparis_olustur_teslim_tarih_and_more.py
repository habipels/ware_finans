# Generated by Django 4.1.2 on 2023-10-27 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0076_siparis_olustur_teslim_tarih'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='teslim_tarih',
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='teslim_sekli',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Teslim Şekli'),
        ),
    ]