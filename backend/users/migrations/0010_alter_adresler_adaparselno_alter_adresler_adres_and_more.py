# Generated by Django 4.1.2 on 2023-06-18 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_adresler'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adresler',
            name='adaparselno',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ADA Parsel No'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='adres',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Adres'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='bulvar',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Bulvar'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='cadde',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Cadde'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='diskapino',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Dış Kapı No'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='ickapino',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='İç Kapı No'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='il',
            field=models.CharField(blank=True, choices=[('istanbul', 'istanbul'), ('Van', 'Van'), ('Ankara', 'Ankara'), ('Batman', 'Batman'), ('Mersin', 'Mersin')], default='Van', max_length=50, null=True, verbose_name='İl'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='ilce',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='İlçe'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='mahhalle_koy',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Mahalle Köy'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='posta_kodu',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Posta Kodu'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='semt',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Semt'),
        ),
        migrations.AlterField(
            model_name='adresler',
            name='sokak',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Sokak'),
        ),
    ]
