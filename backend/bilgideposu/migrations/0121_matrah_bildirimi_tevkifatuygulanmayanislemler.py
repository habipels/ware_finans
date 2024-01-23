# Generated by Django 4.1.2 on 2024-01-23 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_paketler'),
        ('bilgideposu', '0120_kdv1_beyannamesi_bilgileri'),
    ]

    operations = [
        migrations.CreateModel(
            name='matrah_bildirimi_tevkifatuygulanmayanislemler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matrah', models.FloatField(default=0, verbose_name='Matrah')),
                ('kdv', models.FloatField(default=0, verbose_name='KDV')),
                ('vergi', models.FloatField(default=0, verbose_name='Vergi')),
                ('matrah1', models.FloatField(default=0, verbose_name='Matrah')),
                ('kdv1', models.FloatField(default=0, verbose_name='KDV')),
                ('vergi1', models.FloatField(default=0, verbose_name='Vergi')),
                ('matrah2', models.FloatField(default=0, verbose_name='Matrah')),
                ('kdv2', models.FloatField(default=0, verbose_name='KDV')),
                ('vergi2', models.FloatField(default=0, verbose_name='Vergi')),
                ('bagli_oldugu_beyanname', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.kdv1_beyannamesi_bilgileri')),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
            ],
        ),
    ]
