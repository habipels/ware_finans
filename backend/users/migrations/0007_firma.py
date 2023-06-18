# Generated by Django 4.1.2 on 2023-06-18 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customuser_firma_adi'),
    ]

    operations = [
        migrations.CreateModel(
            name='firma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firma_unvani', models.CharField(max_length=100, verbose_name='Firma Unvanı (ADI)')),
                ('Firma_unvani2', models.CharField(max_length=100, verbose_name='Firma Unvanı (Soyadı)')),
                ('silinme_bilgisi', models.BooleanField(default=False)),
                ('firma_muhasabecisi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
