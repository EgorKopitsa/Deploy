# Generated by Django 3.1.2 on 2020-11-06 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0014_auto_20201105_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='shoes',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='top',
            name='image',
            field=models.ImageField(null=True, upload_to='', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='carousel',
            name='images',
            field=models.ImageField(upload_to='', verbose_name='Изображение (1110х360)'),
        ),
        migrations.DeleteModel(
            name='GalleryInline',
        ),
    ]
