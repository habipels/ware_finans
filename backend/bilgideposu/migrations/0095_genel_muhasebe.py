# Generated by Django 4.1.2 on 2023-12-15 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_sgk_bolgecalisma_mudurlukleri_iskurbilgileri'),
        ('bilgideposu', '0094_fatura_durumlari_banka'),
    ]

    operations = [
        migrations.CreateModel(
            name='genel_muhasebe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fis_tarihi', models.DateField(blank=True, null=True, verbose_name='Fiş Tarihi')),
                ('fis_no', models.CharField(blank=True, max_length=200, null=True, verbose_name='Fiş No')),
                ('yevmiye_no', models.CharField(blank=True, max_length=200, null=True, verbose_name='yevmiye No')),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
            ],
        ),
    ]