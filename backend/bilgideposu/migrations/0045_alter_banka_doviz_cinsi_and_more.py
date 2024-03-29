# Generated by Django 4.1.2 on 2023-10-06 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0044_stok_birim_alis_satis_birimi_serinokullan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banka',
            name='doviz_cinsi',
            field=models.CharField(blank=True, choices=[('', ''), ('TL', 'TL'), ('Euro', '£'), ('Dolar', '$')], default='', max_length=100, null=True, verbose_name='Döviz Cinsi'),
        ),
        migrations.AlterField(
            model_name='kasafisislemleri',
            name='islem_turu',
            field=models.CharField(choices=[('', ''), ('Tahsilat Fişi', 'Tahsilat Fişi'), ('Ödeme Fişi', 'Ödeme Fişi'), ('Virman Fişi', 'Virman Fişi'), ('Döviz Fişi', 'Döviz Fişi'), ('Açılış Fişi', 'Açılış Fişi'), ('Kasa Tahsilat Makbuzu', 'Kasa Tahsilat Makbuzu'), ('Kasa Ödeme Makbuzu', 'Kasa Ödeme Makbuzu'), ('Maaş Ödeme (Kasa)', 'Maaş Ödeme (Kasa)'), ('Cari Ödeme Fişi', 'Cari Ödeme Fişi'), ('Cari Tahsilat Fişi', 'Cari Tahsilat Fişi'), ('Cari Maaş Ödemesi (Kasa)', 'Cari Maaş Ödemesi (Kasa)'), ('Bankaya Yatırılan', 'Bankaya Yatırılan'), ('Bankadan Çekilen', 'Bankadan Çekilen'), ('Çek/Senet Tahsili', 'Çek/Senet Tahsili'), ('Senet Ödemesi', 'Senet Ödemesi')], default='', max_length=200, verbose_name='İşlem Türü'),
        ),
    ]
