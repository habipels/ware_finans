# Generated by Django 4.1.2 on 2023-10-05 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0042_alter_stok_kartlar_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='stok_kartlar',
            name='stok_adi',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Stok Adı'),
        ),
    ]
