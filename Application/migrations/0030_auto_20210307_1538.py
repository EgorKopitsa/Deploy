# Generated by Django 3.1.2 on 2021-03-07 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0029_auto_20210307_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='Application.CartProduct'),
        ),
    ]
