# Generated by Django 4.1.2 on 2024-01-27 00:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_paketler'),
        ('bilgideposu', '0133_tam_istisnaa_durumu'),
    ]

    operations = [
        migrations.CreateModel(
            name='istegebaglitamtevkifat_giren_islemler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teslim_ve_hizmet', models.FloatField(default=0, verbose_name='Matrah')),
                ('iadeye_konu_olan_kdv', models.FloatField(default=0, verbose_name='KDV')),
                ('bagli_oldugu_beyanname', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.kdv1_beyannamesi_bilgileri')),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
                ('islem_turu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.tevkifat_tur_kodu')),
            ],
        ),
    ]
