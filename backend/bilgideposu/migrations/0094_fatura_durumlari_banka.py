# Generated by Django 4.1.2 on 2023-12-02 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bilgideposu', '0093_fatura_durumlari_fatura_tipi'),
    ]

    operations = [
        migrations.AddField(
            model_name='fatura_durumlari',
            name='banka',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.banka', verbose_name='Banka Bilgisi'),
        ),
    ]
