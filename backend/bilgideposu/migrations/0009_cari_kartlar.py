# Generated by Django 4.1.2 on 2023-07-07 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0008_kasa'),
    ]

    operations = [
        migrations.CreateModel(
            name='cari_kartlar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ana_cari_kodu', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ana Cari Kodu')),
                ('detay', models.CharField(blank=True, choices=[('', ''), ('Evet', 'Evet'), ('Hayır', 'Hayır')], default='', max_length=100, null=True, verbose_name='Detay')),
                ('listede_gorunsun', models.CharField(blank=True, choices=[('', ''), ('Evet', 'Evet'), ('Hayır', 'Hayır')], default='', max_length=100, null=True, verbose_name='Listede Görünsün')),
                ('cari_kodu', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cari Kodu')),
                ('mukellefyet_turu', models.CharField(blank=True, choices=[('', ''), ('Tüzel Kişi', 'Tüzel Kişi'), ('Gerçek Kişi', 'Gerçek Kişi')], default='', max_length=100, null=True, verbose_name='Mükelelefiyet Türü')),
                ('tip', models.CharField(blank=True, choices=[('', ''), ('1', '1'), ('2', '2')], default='', max_length=100, null=True, verbose_name='Tip')),
                ('cari_hesap_kilitli', models.CharField(blank=True, choices=[('', ''), ('Evet', 'Evet'), ('Hayır', 'Hayır')], default='', max_length=100, null=True, verbose_name='Cari Hesap Kilitli')),
                ('takip_doviz_cinsi', models.CharField(blank=True, choices=[('', ''), ('TL', 'TL'), ('$', '$'), ('£', '£')], default='', max_length=100, null=True, verbose_name='Takip Döviz Cinsi')),
                ('cari_adi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cari Adı')),
                ('yetkili_adi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Yetkili Adı')),
                ('gorevi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Görevi')),
                ('istihbarat', models.CharField(blank=True, max_length=100, null=True, verbose_name='İstihbarat')),
                ('cari_kart_tipi', models.CharField(blank=True, choices=[('', ''), ('Alıcı', 'Alıcı'), ('Satıcı', 'Satıcı'), ('Her İkisi', 'Her İkisi'), ('Ortak', 'Ortak'), ('Özel Cari', 'Özel Cari'), ('Personel', 'Personel'), ('Palsiyer', 'Palsiyer'), ('Gider', 'Gider'), ('Gelir', 'Gelir'), ('Diğer', 'Diğer'), ('Fason', 'Fason'), ('Üye', 'Üye')], default='', max_length=100, null=True, verbose_name='Cari Kart Tipi')),
                ('borc_tutari', models.CharField(blank=True, default='0', max_length=100, null=True, verbose_name='Borç Tutarı (TL)')),
                ('alacak_tutari', models.CharField(blank=True, default='0', max_length=100, null=True, verbose_name='Alacak Tutarı (TL)')),
                ('bakiye_tutari', models.CharField(blank=True, default='0', max_length=100, null=True, verbose_name='Bakiye Tutarı (TL)')),
                ('ozel_kod_1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Özel Kod 1')),
                ('ozel_kod_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Özel Kod 2')),
                ('satici', models.CharField(blank=True, max_length=100, null=True, verbose_name='Satıcı')),
                ('departman', models.CharField(blank=True, max_length=100, null=True, verbose_name='Departman')),
                ('grup_kod_1', models.CharField(blank=True, max_length=100, null=True, verbose_name='Grup Kod 1')),
                ('grup_kod_2', models.CharField(blank=True, max_length=100, null=True, verbose_name='Grup Kod 2')),
                ('grup_kod_3', models.CharField(blank=True, max_length=100, null=True, verbose_name='Grup Kod 3')),
            ],
        ),
    ]