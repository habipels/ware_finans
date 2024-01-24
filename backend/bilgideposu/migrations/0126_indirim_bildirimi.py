# Generated by Django 4.1.2 on 2024-01-24 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_paketler'),
        ('bilgideposu', '0125_indirimler'),
    ]

    operations = [
        migrations.CreateModel(
            name='indirim_bildirimi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kdvorani1', models.FloatField(default=0, verbose_name='Matrah')),
                ('kdvtutari1', models.FloatField(default=0, verbose_name='Vergi')),
                ('kdvorani2', models.FloatField(default=0, verbose_name='Matrah')),
                ('kdvtutari2', models.FloatField(default=0, verbose_name='Vergi')),
                ('kdvorani3', models.FloatField(default=0, verbose_name='Matrah')),
                ('kdvtutari3', models.FloatField(default=0, verbose_name='Vergi')),
                ('bagli_oldugu_beyanname', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bilgideposu.kdv1_beyannamesi_bilgileri')),
                ('bagli_oldugu_firma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.firma')),
            ],
        ),
    ]
