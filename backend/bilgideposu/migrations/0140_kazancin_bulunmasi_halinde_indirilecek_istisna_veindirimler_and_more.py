# Generated by Django 4.1.2 on 2024-02-06 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0139_saglikhizmetindenfaydalananisletmeadi_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='kazancin_bulunmasi_halinde_indirilecek_istisna_veindirimler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icerik', models.CharField(blank=True, max_length=200, null=True, verbose_name='İçerik Bilgisi')),
            ],
        ),
        migrations.CreateModel(
            name='zarar_olsa_dahi_indilicekistisnaveindirim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icerik', models.CharField(blank=True, max_length=200, null=True, verbose_name='İçerik Bilgisi')),
            ],
        ),
    ]
