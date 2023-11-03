# Generated by Django 4.1.2 on 2023-11-03 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_sgk_bolgecalisma_mudurlukleri_iskurbilgileri'),
        ('bilgideposu', '0085_irsaliyeislem_durumlari'),
    ]

    operations = [
        migrations.CreateModel(
            name='irsaliye_olustur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.CharField(blank=True, max_length=200, null=True, verbose_name='tip')),
                ('teslim_tarihi', models.DateField(blank=True, null=True, verbose_name='Kayıt Tarihi')),
                ('teslim_sekli', models.CharField(blank=True, max_length=200, null=True, verbose_name='Teslim Şekli')),
                ('miktar', models.FloatField(blank=True, default=1, null=True, verbose_name='Miktar')),
                ('kalan_miktar', models.FloatField(blank=True, default=1, null=True, verbose_name='Miktar')),
                ('birim', models.CharField(blank=True, max_length=200, null=True, verbose_name='Birim')),
                ('birim_fiyat_tl', models.FloatField(blank=True, default=1, null=True, verbose_name='Birim Fiyatı TL')),
                ('birim_fiyat_dvz', models.FloatField(blank=True, default=1, null=True, verbose_name='Birim Fiyatı Döviz')),
                ('indirim_yuzdesi', models.FloatField(blank=True, default=0, null=True, verbose_name='İndirim Yüzdesi')),
                ('indirim_tutari_tl', models.FloatField(blank=True, default=0, null=True, verbose_name='İndirim Tutarı TL')),
                ('kdv_yuzdesi', models.FloatField(blank=True, default=0, null=True, verbose_name='KDV Yüzdesi')),
                ('kdv_tutari_tl', models.FloatField(blank=True, default=0, null=True, verbose_name='KDV Tutarı TL')),
                ('otv_yuzdesi', models.FloatField(blank=True, default=0, null=True, verbose_name='ÖTV Yüzdesi')),
                ('otv_tutari_tl', models.FloatField(blank=True, default=0, null=True, verbose_name='ÖTV Tutarı TL')),
                ('stoktutari', models.FloatField(blank=True, default=0, null=True, verbose_name='Stok Tutarı TL')),
                ('durumu', models.CharField(blank=True, max_length=200, null=True, verbose_name='Durum')),
                ('indirim1', models.FloatField(blank=True, null=True, verbose_name='İndirim 1')),
                ('indirim2', models.FloatField(blank=True, null=True, verbose_name='İndirim 2')),
                ('indirim3', models.FloatField(blank=True, null=True, verbose_name='İndirim 3')),
                ('ozelkod1', models.CharField(blank=True, max_length=200, null=True, verbose_name='Özel Kod')),
                ('ozelkod2', models.CharField(blank=True, max_length=200, null=True, verbose_name='Özel Kod 2')),
                ('departman', models.CharField(blank=True, max_length=200, null=True, verbose_name='Departman')),
                ('satir_aciklamasi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Satır Açıklaması')),
                ('serino', models.CharField(blank=True, max_length=100, null=True, verbose_name='Seri No')),
                ('s_brim', models.CharField(blank=True, max_length=100, null=True, verbose_name='Serbest Brim')),
                ('s_miktar', models.FloatField(blank=True, default=1, null=True, verbose_name='Serbest Miktar')),
                ('alternatifstokkodu', models.CharField(blank=True, max_length=100, null=True, verbose_name='alternatif stok kodu')),
                ('alternatifstokadi', models.CharField(blank=True, max_length=200, null=True, verbose_name='alternatif stok adı')),
                ('kalite', models.CharField(blank=True, max_length=200, null=True, verbose_name='Kalite')),
                ('ozellik1', models.CharField(blank=True, max_length=200, null=True, verbose_name='ozellil1')),
                ('ozellik2', models.CharField(blank=True, max_length=200, null=True, verbose_name='ozellil2')),
                ('ozellik3', models.CharField(blank=True, max_length=200, null=True, verbose_name='ozellil3')),
                ('ozellik4', models.CharField(blank=True, max_length=200, null=True, verbose_name='ozellil4')),
                ('ozellik5', models.CharField(blank=True, max_length=200, null=True, verbose_name='ozellil5')),
                ('net_agirlik_kg', models.FloatField(blank=True, default=1, null=True, verbose_name='Net Ağırlık KG')),
                ('Burut_agirlik_kg', models.FloatField(blank=True, default=1, null=True, verbose_name='Bürüt Ağırlık KG')),
                ('pk_miktari', models.FloatField(blank=True, default=1, null=True, verbose_name='Pk Miktarı')),
                ('pk_aciklamasi', models.CharField(blank=True, max_length=200, null=True, verbose_name='PK Açıklaması')),
                ('parti_kodu', models.CharField(blank=True, max_length=200, null=True, verbose_name='Parti Kodu')),
                ('son_kullanim_tarihi', models.DateField(blank=True, null=True, verbose_name='Kayıt Tarihi')),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
                ('grup_kodu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.siparisislem_durumlari', verbose_name='Grup Kodu')),
                ('stok_karti_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.stok_kartlar', verbose_name='Stok Kartı Bilgisi')),
            ],
        ),
    ]
