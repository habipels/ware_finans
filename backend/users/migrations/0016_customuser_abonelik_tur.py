# Generated by Django 4.1.2 on 2023-07-07 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_ortak_is_bilgileri_arac_plaka_no1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='abonelik_tur',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='0', max_length=100),
        ),
    ]
