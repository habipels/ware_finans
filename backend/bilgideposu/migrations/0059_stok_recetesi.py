# Generated by Django 4.1.2 on 2023-10-17 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0058_stok_detaylari'),
    ]

    operations = [
        migrations.CreateModel(
            name='stok_recetesi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brim_en', models.FloatField(blank=True, null=True, verbose_name='Brim En')),
                ('brim_boy', models.FloatField(blank=True, null=True, verbose_name='Brim Boy')),
                ('brim_kalinlik', models.FloatField(blank=True, null=True, verbose_name='Brim Kalınlık')),
                ('brim_bolunme_katsayisi', models.FloatField(blank=True, null=True, verbose_name='Brim Bölünme Katsayısı')),
                ('brim_cevrilecek_brim', models.FloatField(blank=True, null=True, verbose_name='Brim Çevrilecek Brim')),
                ('brim_islem_sonucu', models.FloatField(blank=True, null=True, verbose_name='Brim İşlem Sonucu')),
                ('stok_brimi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Stok Brimi')),
                ('ozgul_agirlik', models.CharField(blank=True, max_length=200, null=True, verbose_name='Özgül Ağırlık')),
                ('islem', models.CharField(blank=True, max_length=200, null=True, verbose_name='İşlem')),
                ('recete_miktari', models.CharField(blank=True, max_length=200, null=True, verbose_name='Reçete Miktarı')),
                ('recete_brim_maliyeti', models.CharField(blank=True, max_length=200, null=True, verbose_name='Reçete Brim Maliyeti')),
                ('f_r', models.BooleanField(default=False, verbose_name='FR')),
                ('brim_bilgisi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Brim Bilgisi')),
                ('tur', models.CharField(blank=True, max_length=200, null=True, verbose_name='Tür')),
                ('miktar', models.FloatField(blank=True, null=True, verbose_name='Miktarı')),
                ('doviz_cinsi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Döviz Cinsi')),
                ('brim_fiyati_tl', models.FloatField(blank=True, null=True, verbose_name='Birim Fiyatı TL')),
                ('birim_fiyati_dvz', models.FloatField(blank=True, null=True, verbose_name='Birim Fiyati Döviz')),
                ('fire_yuzdesi', models.FloatField(blank=True, null=True, verbose_name='Fire Yüzdesi')),
                ('fire_miktari', models.FloatField(blank=True, null=True, verbose_name='Fire Miktarı')),
                ('gider_yuzdesi', models.FloatField(blank=True, null=True, verbose_name='Gider Yüzdesi')),
                ('son_guncelleme_tarihi', models.DateField(blank=True, null=True, verbose_name='Son Güncelleme Tarihi')),
                ('satis_aninda_miktar_kadar_uretim_yap', models.BooleanField(default=False, verbose_name='Satış Anında Miktar Kadar Üretim Yap')),
                ('uretimden_giriste_sarf_kaydi_yap', models.BooleanField(default=False, verbose_name='Satış Anında Miktar Kadar Üretim Yap')),
                ('sarf_kaydi_hesaplama_yontemi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Sarf Kaydı Hesaplama Yöntemi')),
                ('alternatif_stok_kodu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stok_alternatif_stok_kodu_set', to='bilgideposu.stok_kartlar', verbose_name='Stok Kartı')),
                ('stok_karti_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stok_recetesi_karti_set', to='bilgideposu.stok_kartlar', verbose_name='Stok Kartı Bilgisi')),
                ('stok_kodu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stok_stok_kodu_set', to='bilgideposu.stok_kartlar', verbose_name='Stok Kartı')),
            ],
        ),
    ]