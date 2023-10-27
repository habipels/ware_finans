# Generated by Django 4.1.2 on 2023-10-27 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_sgk_bolgecalisma_mudurlukleri_iskurbilgileri'),
        ('bilgideposu', '0073_siparis_olustur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='cari_unvan',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='depo',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='ent_kodu',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='islem_doviz_cinsi',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='kdv_durumu',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='ozel_kod1',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='ozel_kod2',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='satici',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='siparis_no',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='siparis_tur',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='sube_kodu',
        ),
        migrations.RemoveField(
            model_name='siparis_olustur',
            name='tarih',
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='cari_unvan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.cari_kartlar', verbose_name='Cari Unvan Bilgisi'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='departman',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='departman'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='depo',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Depo Adı'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='ent_kodu',
            field=models.CharField(choices=[('1', '1'), ('2', '2')], default='1', max_length=20, verbose_name='Entegrasyon Kodu'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='faturaya_aktar',
            field=models.BooleanField(default=False, verbose_name='Faturaya Aktarıldı'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='gunluk_kur',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Günlük Kur'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='irsaliyeye_aktar',
            field=models.BooleanField(default=False, verbose_name='irsaliyey Aktarıldı'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='islem_doviz_cinsi',
            field=models.CharField(choices=[('', ''), ('TL', 'TL'), ('Euro', '£'), ('Dolar', '$')], default='', max_length=100, verbose_name='İşlem Döviz Cinsi'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='kdv_durumu',
            field=models.CharField(choices=[('Hariç', 'Hariç'), ('Dahil', 'Dahil')], default='Hariç', max_length=200, verbose_name='KDV Durumu'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='onay',
            field=models.BooleanField(default=False, verbose_name='Sipariş Onaylandı'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='ozel_kod1',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Özel Kod'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='ozel_kod2',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Özel Kod 2'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='satici',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='SAtıcı'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='siparis_no',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Sipariş No'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='siparis_tur',
            field=models.CharField(choices=[('', ''), ('Alınan Sipariş', 'Alınan Sipariş'), ('Verilen Sipariş', 'Verilen Sipariş'), ('Alınan Teklif', 'Alınan Teklif'), ('Verilen Teklif', 'Verilen Teklif')], default='', max_length=200, verbose_name='Sipariş Türü'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='sube_kodu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.sube', verbose_name='Şube Bilgisi'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='tarih',
            field=models.DateField(blank=True, null=True, verbose_name='Kayıt Tarihi'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='tutar_doviz',
            field=models.FloatField(blank=True, null=True, verbose_name='Tutar Döviz'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='tutar_tl',
            field=models.FloatField(blank=True, null=True, verbose_name='Tutar TL'),
        ),
        migrations.AddField(
            model_name='siparisislem_durumlari',
            name='uygun_kur',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Uygun Kur'),
        ),
    ]
