# Generated by Django 4.1.2 on 2023-09-29 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_sgk_bolgecalisma_mudurlukleri_iskurbilgileri'),
        ('bilgideposu', '0010_kasa_silinme_bilgisi_alter_kasa_doviz_cinsi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cari_kartlar',
            name='cari_adi',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Cari Adı'),
        ),
        migrations.AlterField(
            model_name='cari_kartlar',
            name='takip_doviz_cinsi',
            field=models.CharField(blank=True, choices=[('', ''), ('TL', 'TL'), ('Euro', '£'), ('Dolar', '$')], default='', max_length=100, null=True, verbose_name='Takip Döviz Cinsi'),
        ),
        migrations.CreateModel(
            name='Giderler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ana_gider_kodu', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ana Gider Kodu')),
                ('gider_kodu', models.CharField(blank=True, max_length=100, null=True, verbose_name='gider Kodu')),
                ('gider_adi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Gİder Adı')),
                ('detay', models.CharField(blank=True, choices=[('', ''), ('Evet', 'Evet'), ('Hayır', 'Hayır')], default='', max_length=100, null=True, verbose_name='Detay')),
                ('birim', models.CharField(blank=True, max_length=200, null=True, verbose_name='birim')),
                ('kdv', models.BigIntegerField(blank=True, null=True, verbose_name='KDV (%)')),
                ('doviz_cinsi', models.CharField(blank=True, choices=[('', ''), ('TL', 'TL'), ('Euro', '£'), ('Dolar', '$')], default='', max_length=100, null=True, verbose_name='Döviz Cinsi')),
                ('birim_fiyat_tl', models.CharField(blank=True, max_length=200, null=True, verbose_name='birim Fiyat TL')),
                ('birim_fiyat_doviz', models.CharField(blank=True, max_length=200, null=True, verbose_name='birim Fiyat Döviz')),
                ('ozel_kod_1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Özel Kod 1')),
                ('toplam_alacak', models.CharField(blank=True, max_length=100, null=True, verbose_name='Toplam Tahsilat')),
                ('toplam_borc', models.CharField(blank=True, max_length=100, null=True, verbose_name='Toplam Ödeme')),
                ('toplam_bakiye', models.CharField(blank=True, max_length=100, null=True, verbose_name='Bakiye')),
                ('muh_kodu1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Muh Kodu 1')),
                ('muh_kodu2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Muh Kodu 2')),
                ('muh_kodukdv', models.CharField(blank=True, max_length=100, null=True, verbose_name='Muh Kodu KDV')),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
            ],
        ),
        migrations.CreateModel(
            name='Gelirler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ana_gelir_kodu', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ana gelir Kodu')),
                ('gelir_kodu', models.CharField(blank=True, max_length=100, null=True, verbose_name='gelir Kodu')),
                ('gelir_adi', models.CharField(blank=True, max_length=200, null=True, verbose_name='gelir Adı')),
                ('detay', models.CharField(blank=True, choices=[('', ''), ('Evet', 'Evet'), ('Hayır', 'Hayır')], default='', max_length=100, null=True, verbose_name='Detay')),
                ('birim', models.CharField(blank=True, max_length=200, null=True, verbose_name='birim')),
                ('kdv', models.BigIntegerField(blank=True, null=True, verbose_name='KDV (%)')),
                ('doviz_cinsi', models.CharField(blank=True, choices=[('', ''), ('TL', 'TL'), ('Euro', '£'), ('Dolar', '$')], default='', max_length=100, null=True, verbose_name='Döviz Cinsi')),
                ('birim_fiyat_tl', models.CharField(blank=True, max_length=200, null=True, verbose_name='birim Fiyat TL')),
                ('birim_fiyat_doviz', models.CharField(blank=True, max_length=200, null=True, verbose_name='birim Fiyat Döviz')),
                ('ozel_kod_1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Özel Kod 1')),
                ('toplam_alacak', models.CharField(blank=True, max_length=100, null=True, verbose_name='Toplam Tahsilat')),
                ('toplam_borc', models.CharField(blank=True, max_length=100, null=True, verbose_name='Toplam Ödeme')),
                ('toplam_bakiye', models.CharField(blank=True, max_length=100, null=True, verbose_name='Bakiye')),
                ('muh_kodu1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Muh Kodu 1')),
                ('muh_kodu2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Muh Kodu 2')),
                ('aciklama', models.TextField(blank=True, null=True, verbose_name='Açıklama')),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
            ],
        ),
    ]
