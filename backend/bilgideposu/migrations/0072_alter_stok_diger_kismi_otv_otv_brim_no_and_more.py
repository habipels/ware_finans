# Generated by Django 4.1.2 on 2023-10-26 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0071_stok_diger_kismi_otv_otv_brim_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stok_diger_kismi_otv',
            name='otv_brim_no',
            field=models.FloatField(blank=True, null=True, verbose_name='ÖTV Brim No'),
        ),
        migrations.AlterField(
            model_name='stok_recetesi',
            name='brim_cevrilecek_brim',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Brim Çevrilecek Brim'),
        ),
    ]
