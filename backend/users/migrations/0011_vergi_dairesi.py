# Generated by Django 4.1.2 on 2023-06-18 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_adresler_adaparselno_alter_adresler_adres_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='vergi_dairesi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vergi_dairesi_adi', models.CharField(max_length=200, verbose_name='Vewrigi Dairesi')),
                ('vergi_dairesi_kodu', models.CharField(max_length=100, verbose_name='Vergi Dairesi Kodu')),
            ],
        ),
    ]
