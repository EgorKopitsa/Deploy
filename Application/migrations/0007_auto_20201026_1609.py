# Generated by Django 3.1.2 on 2020-10-26 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0006_carousel'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery',
            field=models.CharField(choices=[('Россия', 'Россия'), ('Другие страны', 'Другие страны')], default='Россия', max_length=100, verbose_name='Доставка'),
        ),
        migrations.AlterField(
            model_name='button',
            name='dimensions',
            field=models.CharField(blank=True, max_length=255, verbose_name='Размеры (через один пробел, без запятых)'),
        ),
        migrations.AlterField(
            model_name='shoes',
            name='dimensions',
            field=models.CharField(blank=True, max_length=255, verbose_name='Размеры (через один пробел, без запятых)'),
        ),
        migrations.AlterField(
            model_name='top',
            name='dimensions',
            field=models.CharField(blank=True, max_length=255, verbose_name='Размеры (через один пробел, без запятых)'),
        ),
    ]
