# Generated by Django 4.1.2 on 2023-12-02 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0092_cek_senet_durumu'),
    ]

    operations = [
        migrations.AddField(
            model_name='fatura_durumlari',
            name='fatura_tipi',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Açık Kapalı'),
        ),
    ]