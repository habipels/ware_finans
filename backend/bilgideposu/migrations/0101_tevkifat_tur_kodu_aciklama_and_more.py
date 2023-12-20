# Generated by Django 4.1.2 on 2023-12-20 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_sgk_bolgecalisma_mudurlukleri_iskurbilgileri'),
        ('bilgideposu', '0100_hesapplanlari_degistiremez_bilgisi'),
    ]

    operations = [
        migrations.AddField(
            model_name='tevkifat_tur_kodu',
            name='aciklama',
            field=models.TextField(blank=True, null=True, verbose_name='Açıklama'),
        ),
        migrations.AddField(
            model_name='tevkifat_tur_kodu',
            name='bagli_oldugu_firma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma'),
        ),
        migrations.AddField(
            model_name='tevkifat_tur_kodu',
            name='degistiremez_bilgisi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tevkifat_tur_kodu',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False),
        ),
    ]
