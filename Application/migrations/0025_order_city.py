# Generated by Django 3.1.2 on 2021-01-25 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0024_auto_20201122_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.CharField(default='', max_length=255, verbose_name='Город'),
        ),
    ]
