# Generated by Django 4.1.2 on 2023-10-04 01:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0034_kasafisislemleri_cari_unvan'),
    ]

    operations = [
        migrations.AddField(
            model_name='kasafisislemleri',
            name='banka_bilgisi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.banka', verbose_name='Banka Bilgisi'),
        ),
    ]
