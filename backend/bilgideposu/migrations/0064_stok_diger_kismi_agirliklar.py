# Generated by Django 4.1.2 on 2023-10-19 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0063_stok_diger_kismi_otv'),
    ]

    operations = [
        migrations.CreateModel(
            name='stok_diger_kismi_agirliklar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('net', models.FloatField(blank=True, null=True, verbose_name='NET')),
                ('brut', models.FloatField(blank=True, null=True, verbose_name='Brüt')),
                ('dara', models.FloatField(blank=True, null=True, verbose_name='Dara')),
                ('p_miktari', models.FloatField(blank=True, null=True, verbose_name='P miktari')),
                ('p_aciklamasi', models.TextField(blank=True, null=True, verbose_name='P Açıklması')),
                ('stok_karti_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stok_diger_kismi_agirliklar_set', to='bilgideposu.stok_kartlar', verbose_name='Stok Kartı Bilgisi')),
            ],
        ),
    ]
