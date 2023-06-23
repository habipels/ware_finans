# Generated by Django 4.1.2 on 2023-06-23 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_adresler_silinme_bilgisi_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='arac_plaka_no1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Araç Plaka No 1'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='arac_plaka_no2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Araç Plaka No 2'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='arac_plaka_no3',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Araç Plaka No 3'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='bagkur_basamagi',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Bağkur Başamağı'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='bagkur_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Bağkur Numarası'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='ceptelefon1',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Cep Telefon Numarası '),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='ceptelefon2',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Cep Telefon Numarası 2'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='dernek_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Dernek No'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='diger_isyeri_tescil_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Diğer İşyeri Tescil No'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='emekli_sandigi_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Emekli Sandığı No'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='eposta',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email Adresi'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='evtelefon',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Ev Telefon Numarası '),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='faliyet_kodu',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Faliyet Kodu'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='faliyet_suresi',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Faliyet Süresi'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='fax',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Fax Adresi'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='istelefonu',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='İş Telefon Numarası'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='istelefonu2',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='İş Telefon Numarası 2'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='isyeri_adrsi',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='İşyeri Adresi'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='isyeri_postakodu',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='İşyeri Posta Kodu'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='meslegi',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Mesleği'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='meslek_tesekkul_adi',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Meslek Teşekkül Adı'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='mesleki_tesekkulno',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Meslek Teşekkül No'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='ssk_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='SSK NO'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='vakif_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Vakıf No'),
        ),
        migrations.AlterField(
            model_name='ortak_is_bilgileri',
            name='web_adrsi',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Web Adresi'),
        ),
        migrations.CreateModel(
            name='ortak_kimlik_bilgileri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adi_soyadi', models.CharField(max_length=100, verbose_name='Adı Soyadı')),
                ('tckimlik', models.CharField(blank=True, max_length=12, null=True, verbose_name='T.C Kimlik No')),
                ('kimlik_seri', models.CharField(blank=True, max_length=20, null=True, verbose_name='T.C Kimlik Seri No')),
                ('kimlik_no', models.CharField(blank=True, max_length=100, null=True, verbose_name='Kimlik No')),
                ('baba_adi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Baba Adı')),
                ('anne_adi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Anne Adı')),
                ('dogum_yeri', models.CharField(blank=True, max_length=100, null=True, verbose_name='Doğum Yeri')),
                ('dogum_tarihi', models.DateField(blank=True, null=True, verbose_name='Doğum Tarihi')),
                ('cinsiyet', models.CharField(choices=[('', ''), ('Erkek', 'Erkek'), ('Kadın', 'Kadın')], default='', max_length=100, verbose_name='Cinsiyet')),
                ('anne_kizlık_soyadi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Anne Kızlık Soyadı')),
                ('medeni_hali', models.CharField(choices=[('', ''), ('Evli', 'Evli'), ('Bekar', 'Bekar')], default='', max_length=100, verbose_name='Medeni Hali')),
                ('evlilik_tarihi', models.DateField(blank=True, null=True, verbose_name='Evlilik Tarihi')),
                ('onceki_soyadi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Önceki Soyadı')),
                ('uyruğu_yabanci_ise_ulkesi', models.CharField(blank=True, max_length=100, null=True, verbose_name='Uyruğu Yabancı İse Ülkesi')),
                ('kan_grubu', models.CharField(blank=True, max_length=5, null=True, verbose_name='Kan Grubu')),
                ('nufusa_kayitli_koy_mahhalle', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nufusa Kayıtlı Olduğu Köy Mahalle')),
                ('cilt_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='Cilt NO')),
                ('aile_sira_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='Aile Sıra NO')),
                ('sira_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='Sıra NO')),
                ('sayfa_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='Sayfa NO')),
                ('cuzdanin_verildiği_yer', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cüzdanın Verildiği Yer')),
                ('verilis_nedeni', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nufus Cüzdanı Veriliş Nedeni')),
                ('cuzdan_kayit_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='Cüzdan Kayıt No')),
                ('cuzdan_verilis_tarihi', models.DateField(blank=True, null=True, verbose_name='Cüzdan Veriliş Tarihi')),
                ('nufusa_kayitli_il_ilce', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.i̇ller_ve_ilceler', verbose_name='Nufusa KAyıtlı Olduğu İl İlçe')),
                ('ortak_bilgileri', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.ortak_bilgileri')),
            ],
        ),
    ]
