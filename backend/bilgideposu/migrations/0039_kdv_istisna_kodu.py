# Generated by Django 4.1.2 on 2023-10-05 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0038_kasafisislemleri_kendisi_secme'),
    ]

    operations = [
        migrations.CreateModel(
            name='kdv_istisna_kodu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kod', models.CharField(blank=True, max_length=100, null=True, verbose_name='KDV İstisna Kodu')),
                ('icerik', models.CharField(blank=True, max_length=200, null=True, verbose_name='KDV İstisna Yazısı')),
            ],
        ),
    ]
