# Generated by Django 4.1.2 on 2023-09-29 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0013_cari_kartlar_bagli_oldugu_firma'),
    ]

    operations = [
        migrations.AddField(
            model_name='cari_kartlar',
            name='silinme_bilgisi',
            field=models.BooleanField(default=False),
        ),
    ]
