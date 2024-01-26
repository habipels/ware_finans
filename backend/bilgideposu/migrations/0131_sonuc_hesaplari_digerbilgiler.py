# Generated by Django 4.1.2 on 2024-01-26 14:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_paketler'),
        ('bilgideposu', '0130_sonuc_hesaplari'),
    ]

    operations = [
        migrations.CreateModel(
            name='sonuc_hesaplari_digerbilgiler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sonucyazisidiger1', models.CharField(blank=True, max_length=200, null=True, verbose_name='sonuç yazısı')),
                ('sonucdiger1', models.FloatField(default=0, verbose_name='sonuctutarı')),
                ('sonucdiger2', models.FloatField(default=0, verbose_name='sonuctutarı')),
                ('sonucyazisidiger2', models.CharField(blank=True, max_length=200, null=True, verbose_name='sonuç yazısı')),
                ('sonucdiger3', models.FloatField(default=0, verbose_name='sonuctutarı')),
                ('sonucyazisidiger3', models.CharField(blank=True, max_length=200, null=True, verbose_name='sonuç yazısı')),
                ('sonucdiger4', models.FloatField(default=0, verbose_name='sonuctutarı')),
                ('sonucyazisidiger4', models.CharField(blank=True, max_length=200, null=True, verbose_name='sonuç yazısı')),
                ('bagli_oldugu_beyanname', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.kdv1_beyannamesi_bilgileri')),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
            ],
        ),
    ]