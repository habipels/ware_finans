# Generated by Django 4.1.2 on 2023-10-25 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0067_dilekceler'),
    ]

    operations = [
        migrations.AddField(
            model_name='dilekceler',
            name='dilekce_adi',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Dilekçe Adı'),
        ),
    ]
