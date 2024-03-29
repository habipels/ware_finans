# Generated by Django 4.1.2 on 2023-10-03 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0024_cari_kartislemleri_sube_bilgiler_subebilgilerisehir_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banka',
            name='muh_kodu',
        ),
        migrations.AlterField(
            model_name='banka',
            name='toplam_bakiye',
            field=models.FloatField(blank=True, null=True, verbose_name='Bakiye'),
        ),
        migrations.AlterField(
            model_name='banka',
            name='toplam_cekilen',
            field=models.FloatField(blank=True, null=True, verbose_name='Toplam Çekilen'),
        ),
        migrations.AlterField(
            model_name='banka',
            name='toplam_yatirilan',
            field=models.FloatField(blank=True, null=True, verbose_name='Toplam Yatırılan'),
        ),
    ]
