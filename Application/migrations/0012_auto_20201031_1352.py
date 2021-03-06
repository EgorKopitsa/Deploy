# Generated by Django 3.1.2 on 2020-10-31 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0011_remove_category_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='button',
            name='material',
            field=models.CharField(default='', max_length=255, verbose_name='Материал'),
        ),
        migrations.AddField(
            model_name='order',
            name='track_number',
            field=models.CharField(default='', max_length=255, verbose_name='Трек номер'),
        ),
        migrations.AddField(
            model_name='shoes',
            name='material',
            field=models.CharField(default='', max_length=255, verbose_name='Материал'),
        ),
        migrations.AddField(
            model_name='top',
            name='material',
            field=models.CharField(default='', max_length=255, verbose_name='Материал'),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(default='', max_length=1024, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Отправлен', 'Отправлен'), ('Оплачен', 'Оплачен'), ('В обработке', 'В обработке'), ('Не оплачен', 'Не оплачен')], default='В обработке', max_length=100, verbose_name='Статус заказа'),
        ),
    ]
