# Generated by Django 4.1.2 on 2023-10-17 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0055_alter_bankafisislemleri_islem_turu_cari_fisleri'),
    ]

    operations = [
        migrations.CreateModel(
            name='stok_alis_satis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('satis_fiyati_1_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 1')),
                ('satis_fiyati_2_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 2')),
                ('satis_fiyati_3_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 3')),
                ('satis_fiyati_4_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 4')),
                ('satis_fiyati_5_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 5')),
                ('satis_fiyati_6_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 6')),
                ('satis_fiyati_7_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 7')),
                ('satis_fiyati_8_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 8')),
                ('satis_fiyati_9_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 9')),
                ('satis_fiyati_10_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 10')),
                ('satis_fiyati_1_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı Döviz 1')),
                ('satis_fiyati_2_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı Döviz 2')),
                ('satis_fiyati_3_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı Döviz 3')),
                ('satis_fiyati_4_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı Döviz 4')),
                ('satis_fiyati_5_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı Döviz 5')),
                ('satis_fiyati_6_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı Döviz 6')),
                ('satis_fiyati_7_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı Döviz 7')),
                ('satis_fiyati_8_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı Döviz 8')),
                ('satis_fiyati_9_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı Döviz 9')),
                ('satis_fiyati_10_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı Döviz 10')),
                ('aktif_satis_fiyati', models.CharField(blank=True, max_length=20, null=True, verbose_name='Aktif Satış Fiyatı')),
                ('birim_secenegi', models.CharField(blank=True, max_length=20, null=True, verbose_name='Secilen Birim Seçeneği')),
                ('alis_fiyati_1_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 1')),
                ('alis_fiyati_2_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 2')),
                ('alis_fiyati_3_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 3')),
                ('alis_fiyati_4_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 4')),
                ('alis_fiyati_5_tl', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı tl 5')),
                ('alis_fiyati_1_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı dvz 1')),
                ('alis_fiyati_2_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı dvz 2')),
                ('alis_fiyati_3_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı dvz 3')),
                ('alis_fiyati_4_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı dvz 4')),
                ('alis_fiyati_5_dvz', models.FloatField(blank=True, null=True, verbose_name='Satış fiyatı dvz 5')),
                ('aktif_alis_fiyati', models.CharField(blank=True, max_length=20, null=True, verbose_name='Aktif Alış Fiyatı')),
                ('alis_dovizcinsi', models.CharField(blank=True, max_length=20, null=True, verbose_name='Secilen Döviz Seçeneği')),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('maliyet_yontemi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Maliyet Yöntemi')),
                ('satis_kar_evrak', models.CharField(blank=True, max_length=200, null=True, verbose_name='Satış Kar Evrağı')),
                ('satis_kar_yuzdesi', models.FloatField(blank=True, null=True, verbose_name='Satış Kar Yüzdesi')),
                ('stok_karti_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stok_karti_bilgisi_stokalis_satis_set', to='bilgideposu.stok_kartlar', verbose_name='Stok Kartı Bilgisi')),
            ],
        ),
    ]
