# Generated by Django 4.1.2 on 2023-09-24 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_taseronbilgileri_taseronunvanbilgisi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taseronbilgileri',
            name='web_adresi',
        ),
    ]
