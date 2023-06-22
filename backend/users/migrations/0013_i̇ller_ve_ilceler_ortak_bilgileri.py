# Generated by Django 4.1.2 on 2023-06-22 21:42

from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_sube'),
    ]

    operations = [
        migrations.CreateModel(
            name='İller_ve_ilceler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kategory_tr', users.models.user_adi(max_length=100, verbose_name='İl veya İlçe ')),
                ('link', users.models.kategory_link_ayari(max_length=200)),
                ('keywords', models.CharField(max_length=255)),
                ('ust_kategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='users.i̇ller_ve_ilceler', verbose_name='İlçe İse İli Şecin')),
            ],
        ),
        migrations.CreateModel(
            name='ortak_bilgileri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unvan', models.CharField(blank=True, choices=[('işveren', 'işveren'), ('Yönetici', 'Yönetici'), ('Ortak', 'Ortak'), ('İşveren Vekil', 'İşveren Vekil')], default='işveren', max_length=100, null=True, verbose_name='Unvan Bilgisi')),
                ('vekil_ortak', models.CharField(blank=True, choices=[('Ortak', 'Ortak'), ('İşveren Vekil', 'İşveren Vekil')], default='Ortak', max_length=100, null=True, verbose_name='vekil Ortaklık Bilgisi')),
                ('ortaklik_giris_tarihi', models.DateField(blank=True, null=True, verbose_name='Ortaklık Giriş Tarihi')),
                ('ortakliktan_cikis_tarihi', models.DateField(blank=True, null=True, verbose_name='Ortaklıktan Çıkış Tarihi')),
                ('goreve_baslama_tarihi', models.DateField(blank=True, null=True, verbose_name='Göreve Başlama Tarihi')),
                ('gorevi_bitirme_tarihi', models.DateField(blank=True, null=True, verbose_name='Görevi Bitirme Tarihi')),
                ('hisse_orani', models.BigIntegerField(blank=True, null=True, verbose_name='Hisse Oranı')),
                ('hisse_tutari', models.BigIntegerField(blank=True, null=True, verbose_name='Hisse Tutarı')),
                ('ticaret_sicil_no', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ticaret Sicil No')),
                ('ticaret_sicil_gazetesi_tarihi', models.DateField(blank=True, null=True, verbose_name='Ticaret Sicil Gazetesi Tarihi')),
                ('ticaret_sicil_gazetesi_sayfa_n', models.BigIntegerField(blank=True, null=True, verbose_name='Ticaret Sicil Gazetesi Sayfa No')),
                ('vergi_dairesi_kodu', models.CharField(blank=True, max_length=100, null=True, verbose_name='Vergi Dairesi Kodu')),
                ('vergi_numarasi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Vergi Numarası')),
                ('firma_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma', verbose_name='Firma Bilgisi')),
                ('vergi_dairesi_adi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.vergi_dairesi')),
                ('vergi_dairesi_ili_ilcesi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.i̇ller_ve_ilceler')),
            ],
        ),
    ]
