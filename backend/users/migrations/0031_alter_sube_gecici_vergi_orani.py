# Generated by Django 4.1.2 on 2023-12-28 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_sgk_bolgecalisma_mudurlukleri_iskurbilgileri'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sube',
            name='gecici_vergi_orani',
            field=models.FloatField(blank=True, null=True, verbose_name='Geçici Vergi Oranı %'),
        ),
    ]
