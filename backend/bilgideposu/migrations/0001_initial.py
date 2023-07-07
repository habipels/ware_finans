# Generated by Django 4.1.2 on 2023-06-26 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0015_alter_ortak_is_bilgileri_arac_plaka_no1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='banka',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banka_kodu', models.CharField(blank=True, max_length=100, null=True, verbose_name='Banka Kodu')),
                ('entkodu', models.CharField(blank=True, default='', max_length=10, null=True, verbose_name='Ent Kodu')),
                ('banka_adi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Banka Adı')),
                ('sube_adi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Şube Adı')),
                ('sube_kodu', models.CharField(blank=True, max_length=200, null=True, verbose_name='Şube Kodu')),
                ('hesap_turu', models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Hesap Turu')),
                ('hesap_adi', models.CharField(blank=True, max_length=200, null=True, verbose_name='Hesap Adı')),
                ('hesap_no', models.CharField(blank=True, max_length=200, null=True, verbose_name='Hesap No')),
                ('iban_numarasi', models.CharField(blank=True, max_length=20, null=True, verbose_name='İban Numarası')),
                ('kullanabilir_kredi_tutari', models.CharField(blank=True, max_length=200, null=True, verbose_name='Kullanabilir kredi Tutarı')),
                ('ozel_kod', models.CharField(blank=True, max_length=100, null=True, verbose_name='Özel Kod')),
                ('doviz_cinsi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Döviz Cinsi')),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
            ],
        ),
    ]