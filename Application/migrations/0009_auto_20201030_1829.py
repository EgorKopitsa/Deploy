# Generated by Django 3.1.2 on 2020-10-30 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0008_delivery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Промежуточная корзина', 'verbose_name_plural': 'Промежуточная корзина'},
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', upload_to='', verbose_name='Изображение'),
        ),
    ]
