# Generated by Django 4.1.2 on 2024-02-01 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0137_gecicivergi_beyannamesi_inidimi'),
    ]

    operations = [
        migrations.CreateModel(
            name='iller_ilkodu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('illerilkodu', models.CharField(max_length=200, verbose_name='Açıklama')),
            ],
        ),
    ]
