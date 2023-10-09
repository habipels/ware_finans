# Generated by Django 4.1.2 on 2023-10-09 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_sgk_bolgecalisma_mudurlukleri_iskurbilgileri'),
        ('bilgideposu', '0054_alter_banka_doviz_cinsi_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankafisislemleri',
            name='islem_turu',
            field=models.CharField(choices=[('', ''), ('Virman Fişi', 'Virman Fişi'), ('Döviz Fişi', 'Döviz Fişi'), ('Açılış Fişi', 'Açılış Fişi'), ('Gelir Fişi', 'Gelir Fişi'), ('Gider Fişi', 'Gider Fişi'), ('Faiz Geliri Fişi', 'Faiz Geliri Fişi'), ('Banka Gelir Makbuzu', 'Banka Gelir Makbuzu'), ('Banka Gider Makbuzu', 'Banka Gider Makbuzu'), ('Gönderilen Havale', 'Gönderilen Havale'), ('Gelen Havale', 'Gelen Havale'), ('Cari Maaş Ödemesi (Banka)', 'Cari Maaş Ödemesi (Banka)'), ('Çek/Senet Tescili', 'Çek/Senet Tescili'), ('Çek Ödemesi', 'Çek Ödemesi')], default='', max_length=200, verbose_name='İşlem Türü'),
        ),
        migrations.CreateModel(
            name='cari_fisleri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('islem_turu', models.CharField(choices=[('', ''), ('Borç Dekontu', 'Borç Dekontu'), ('Alacak Dekontu', 'Alacak Dekontu'), ('Ödeme Fişi', 'Ödeme Fişi'), ('Tahsilat Fişi', 'Tahsilat Fişi'), ('Virman Fişi', 'Virman Fişi'), ('Açılış Fişi', 'Açılış Fişi'), ('Maaş Tahakkuku', 'Maaş Tahakkuku'), ('Maaş Ödemesi', 'Maaş Ödemesi'), ('Toplu Dekont', 'Toplu Dekont'), ('Cari Ödeme Makbuzu', 'Cari Ödeme Makbuzu'), ('Cari Tahsilat Makbuzu', 'Cari Tahsilat Makbuzu'), ('Borç Makbuzu', 'Borç Makbuzu'), ('Alacak Makbuzu', 'Alacak Makbuzu'), ('Tahsilat Makbuzu', 'Tahsilat Makbuzu'), ('Ödeme Planı Tahsilatı', 'Ödeme Planı Tahsilatı'), ('Bordrodan Puantaj Al', 'Bordrodan Puantaj Al')], default='', max_length=200, verbose_name='İşlem Türü')),
                ('tarih', models.DateField(blank=True, null=True, verbose_name='İşlem Tarihi')),
                ('saat', models.TimeField(blank=True, null=True, verbose_name='İşlem Saati')),
                ('evrak_no', models.CharField(blank=True, max_length=100, null=True, verbose_name='Evrak Tarihi')),
                ('ent_kodu', models.CharField(choices=[('', ''), ('1', '1'), ('2', '2')], default='', max_length=2, verbose_name='Ent Kodu')),
                ('vade_tarih', models.DateField(blank=True, null=True, verbose_name='Vade Tarihi')),
                ('vade_gunu', models.CharField(blank=True, max_length=100, null=True, verbose_name='Vade Günü')),
                ('ozelkod1', models.CharField(blank=True, max_length=200, null=True, verbose_name='Özel Kod')),
                ('ozelkod2', models.CharField(blank=True, max_length=200, null=True, verbose_name='Özel Kod 2')),
                ('birinci_departman', models.CharField(blank=True, max_length=200, null=True, verbose_name='Departman')),
                ('birinci_cari_muh_kodu', models.CharField(blank=True, max_length=200, null=True, verbose_name='Kasa Muhtasar Kodu')),
                ('gelir_muh_kodu', models.CharField(blank=True, max_length=200, null=True, verbose_name='Gelir Muhtasar Kodu')),
                ('islem_doviz_cinsi', models.CharField(choices=[('', ''), ('TL', 'TL'), ('Euro', 'Euro'), ('Dolar', 'Dolar')], default='', max_length=100, verbose_name='İşlem Döviz Cinsi')),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='İşlem Açıklama ')),
                ('islemi_yapan', models.CharField(blank=True, max_length=250, null=True, verbose_name='İşlemi Yapan')),
                ('tutar', models.FloatField(blank=True, null=True, verbose_name='İşlem Tutarı')),
                ('tutar_tl', models.FloatField(blank=True, null=True, verbose_name='İşlem Tutarı (TL)')),
                ('doviz_tutar', models.FloatField(blank=True, null=True, verbose_name='İşlem Tutarı döviz')),
                ('gider_muh_kodu', models.CharField(blank=True, max_length=200, null=True, verbose_name='Gİder Muhtasar Kodu')),
                ('ikinci_departman', models.CharField(blank=True, max_length=200, null=True, verbose_name='Departman')),
                ('ikinci_cari_muh_kodu', models.CharField(blank=True, max_length=200, null=True, verbose_name='Kasa Muhtasar Kodu')),
                ('islem_durumu', models.BooleanField(default=False, verbose_name='İşlem Tamamlandıysa tikli olacak')),
                ('satici', models.CharField(blank=True, max_length=200, null=True, verbose_name='SAtıcı')),
                ('kampkodu', models.CharField(blank=True, max_length=200, null=True, verbose_name='Kamp Kodu')),
                ('gunluk_kur', models.CharField(blank=True, max_length=200, null=True, verbose_name='Günlük Kur')),
                ('uygun_kur', models.CharField(blank=True, max_length=200, null=True, verbose_name='Uygun Kur')),
                ('alacakbilgisi', models.CharField(blank=True, max_length=200, null=True, verbose_name='alacakbilgisi')),
                ('gider_durumu', models.CharField(blank=True, max_length=100, null=True, verbose_name='Gider Durumu')),
                ('gideryuzdesi', models.FloatField(blank=True, null=True, verbose_name='Gider yüzdesi')),
                ('kasa_banka_muh_kodu', models.CharField(blank=True, max_length=200, null=True, verbose_name='Kasa Muhtasar Kodu')),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('islem_sonucu_bakiye_birinci_cari', models.FloatField(blank=True, null=True, verbose_name='İşlem Sonucu Bakiye')),
                ('islem_sonucu_bakiye_ikinci_cari', models.FloatField(blank=True, null=True, verbose_name='İşlem Sonucu Bakiye')),
                ('islem_sonucu_bakiye_banka', models.FloatField(blank=True, null=True, verbose_name='İşlem Sonucu Bakiye')),
                ('islem_sonucu_bakiye_kasa', models.FloatField(blank=True, null=True, verbose_name='İşlem Sonucu Bakiye')),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
                ('banka_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.kasa', verbose_name='Kasa Bilgisi')),
                ('bankasecme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.banka', verbose_name='Banka Bilgisi')),
                ('birinci_cari_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='birinci_cari_fis_islemleri_set', to='bilgideposu.cari_kartlar', verbose_name='Birinci Cari Bilgisi')),
                ('birinciislem_sube_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='birinciislem_cari_fis_islemleri_set_banka', to='users.sube', verbose_name='Şube')),
                ('gelir_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gelir_cari_fis_islemleri_set', to='bilgideposu.gelirler', verbose_name='Gelir Bilgisi')),
                ('gider_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gider_cari_fis_islemleri_set', to='bilgideposu.giderler', verbose_name='Gelir Bilgisi')),
                ('ikinci_cari_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ikinci_cari_fis_islemleri_set', to='bilgideposu.cari_kartlar', verbose_name='İkinci Kasa Bilgisi')),
                ('ikinci_gelir_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ikinci_gelir_cari_fis_islemleri_set', to='bilgideposu.gelirler', verbose_name='Gelir Bilgisi')),
                ('ikinci_gider_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ikinci_gider_cari_fis_islemleri_set', to='bilgideposu.giderler', verbose_name='Gelir Bilgisi')),
                ('ikinci_islem_sube_bilgisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ikinciislem_cari_fis_islemleri_set', to='users.sube', verbose_name='Şube')),
                ('kendisi_secme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='bilgideposu.cari_fisleri', verbose_name='makbuzlar için')),
            ],
        ),
    ]
