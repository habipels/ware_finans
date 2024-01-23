# Generated by Django 4.1.2 on 2024-01-20 14:48

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_alter_sgk_bilgileri_personel_6116645yararlanmiyorsayenikanun'),
    ]

    operations = [
        migrations.CreateModel(
            name='paketler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paket_adi', models.CharField(max_length=200, verbose_name='PAket Adı')),
                ('paket_fiyati', models.FloatField(default=0, verbose_name='Fiyat Bilgisi')),
                ('icerigi', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='İçeriği Metni')),
            ],
        ),
    ]