# Generated by Django 4.1.2 on 2024-01-06 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0112_delete_demirbaslar'),
    ]

    operations = [
        migrations.AddField(
            model_name='amortisman_bilgileri',
            name='N1',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='N3'),
        ),
        migrations.AddField(
            model_name='amortisman_bilgileri',
            name='N2',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='N3'),
        ),
    ]
