# Generated by Django 3.1.2 on 2020-10-26 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0005_delete_carousel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='', verbose_name='Изображение (900х350)')),
            ],
            options={
                'verbose_name': 'Карусель',
                'verbose_name_plural': 'Карусель',
            },
        ),
    ]
