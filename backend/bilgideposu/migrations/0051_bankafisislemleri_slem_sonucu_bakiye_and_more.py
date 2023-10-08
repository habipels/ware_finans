# Generated by Django 4.1.2 on 2023-10-08 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0050_bankafisislemleri'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankafisislemleri',
            name='slem_sonucu_bakiye',
            field=models.FloatField(blank=True, null=True, verbose_name='İşlem Sonucu Bakiye'),
        ),
        migrations.AddField(
            model_name='kasafisislemleri',
            name='islem_sonucu_bakiye',
            field=models.FloatField(blank=True, null=True, verbose_name='İşlem Sonucu Bakiye'),
        ),
    ]
