# Generated by Django 4.1.2 on 2023-09-16 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_vergi_daireleri'),
    ]

    operations = [
        migrations.DeleteModel(
            name='vergi_daireleri',
        ),
        migrations.AddField(
            model_name='vergi_dairesi',
            name='il',
            field=models.CharField(default=0, max_length=100, verbose_name='İL'),
            preserve_default=False,
        ),
    ]
