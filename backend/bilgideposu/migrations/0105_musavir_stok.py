# Generated by Django 4.1.2 on 2024-01-03 23:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_alter_sgk_bilgileri_personel_6116645yararlanmiyorsayenikanun'),
        ('bilgideposu', '0104_musteri_cari_sininme_bilgisi'),
    ]

    operations = [
        migrations.CreateModel(
            name='musavir_stok',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stok_adi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Stok Adı')),
                ('birim', models.CharField(blank=True, max_length=200, null=True, verbose_name='Birim')),
                ('envanter_yonetimi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Envanter yönetimi')),
                ('ort_kar', models.FloatField(default=0, verbose_name='Ort Kar')),
                ('kayit_tarihi', models.DateTimeField(default=datetime.datetime.now, null=True)),
                ('sininme_bilgisi', models.BooleanField(default=False)),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
            ],
        ),
    ]