# Generated by Django 4.1.2 on 2023-06-23 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_i̇ller_ve_ilceler_ortak_bilgileri'),
    ]

    operations = [
        migrations.AddField(
            model_name='adresler',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ortak_bilgileri',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sube',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ortak_is_bilgileri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bagkur_no', models.CharField(max_length=100, verbose_name='Bağkur Numarası')),
                ('bagkur_basamagi', models.CharField(max_length=100, verbose_name='Bağkur Başamağı')),
                ('ssk_no', models.CharField(max_length=100, verbose_name='SSK NO')),
                ('emekli_sandigi_no', models.CharField(max_length=100, verbose_name='Emekli Sandığı No')),
                ('diger_isyeri_tescil_no', models.CharField(max_length=100, verbose_name='Diğer İşyeri Tescil No')),
                ('vakif_no', models.CharField(max_length=100, verbose_name='Vakıf No')),
                ('dernek_no', models.CharField(max_length=100, verbose_name='Dernek No')),
                ('tutugu_defter_turu', models.CharField(choices=[('', ''), ('Bilanço', 'Bilanço'), ('Diğer Defter', 'Diğer Defter'), ('Deftere Tabi Değil', 'Deftere Tabi Değil')], default='', max_length=100, verbose_name='Tutuğu Defter Türü')),
                ('meslegi', models.CharField(max_length=100, verbose_name='Mesleği')),
                ('faliyet_kodu', models.CharField(max_length=100, verbose_name='Faliyet Kodu')),
                ('faliyet_suresi', models.CharField(max_length=100, verbose_name='Faliyet Süresi')),
                ('meslek_tesekkul_adi', models.CharField(max_length=100, verbose_name='Meslek Teşekkül Adı')),
                ('mesleki_tesekkulno', models.CharField(max_length=100, verbose_name='Meslek Teşekkül No')),
                ('arac_plaka_no1', models.CharField(max_length=100, verbose_name='Araç Plaka No 1')),
                ('arac_plaka_no2', models.CharField(max_length=100, verbose_name='Araç Plaka No 2')),
                ('arac_plaka_no3', models.CharField(max_length=100, verbose_name='Araç Plaka No 3')),
                ('isyeri_adrsi', models.CharField(max_length=200, verbose_name='İşyeri Adresi')),
                ('isyeri_postakodu', models.CharField(max_length=200, verbose_name='İşyeri Posta Kodu')),
                ('istelefonu', models.CharField(max_length=20, verbose_name='İş Telefon Numarası')),
                ('istelefonu2', models.CharField(max_length=20, verbose_name='İş Telefon Numarası 2')),
                ('evtelefon', models.CharField(max_length=20, verbose_name='Ev Telefon Numarası ')),
                ('ceptelefon1', models.CharField(max_length=20, verbose_name='Cep Telefon Numarası ')),
                ('ceptelefon2', models.CharField(max_length=20, verbose_name='Cep Telefon Numarası 2')),
                ('fax', models.CharField(max_length=100, verbose_name='Fax Adresi')),
                ('eposta', models.EmailField(max_length=100, verbose_name='Email Adresi')),
                ('web_adrsi', models.CharField(max_length=100, verbose_name='Web Adresi')),
                ('adress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.adresler')),
                ('il_ilce', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.i̇ller_ve_ilceler')),
                ('ortak_bilgileri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.ortak_bilgileri')),
            ],
        ),
    ]
