# Generated by Django 4.1.2 on 2024-01-24 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0126_indirim_bildirimi'),
    ]

    operations = [
        migrations.AddField(
            model_name='matrah_bildirimi_digerislemleri',
            name='bilgi',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Açıklama'),
        ),
        migrations.AddField(
            model_name='matrah_bildirimi_digerislemleri',
            name='bilgi2',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Açıklama'),
        ),
        migrations.AddField(
            model_name='matrah_bildirimi_digerislemleri',
            name='bilgi3',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Açıklama'),
        ),
        migrations.AddField(
            model_name='matrah_bildirimi_digerislemleri',
            name='bilgi4',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Açıklama'),
        ),
        migrations.AddField(
            model_name='matrah_bildirimi_digerislemleri',
            name='bilgi5',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Açıklama'),
        ),
        migrations.AddField(
            model_name='matrah_bildirimi_digerislemleri',
            name='bilgi6',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Açıklama'),
        ),
        migrations.AddField(
            model_name='matrah_bildirimi_digerislemleri',
            name='bilgi7',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Açıklama'),
        ),
    ]
