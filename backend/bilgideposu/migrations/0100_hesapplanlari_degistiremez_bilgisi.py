# Generated by Django 4.1.2 on 2023-12-15 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0099_alter_hesapplanlari_alacak_toplam_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hesapplanlari',
            name='degistiremez_bilgisi',
            field=models.BooleanField(default=False),
        ),
    ]
