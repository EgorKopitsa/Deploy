# Generated by Django 3.1.2 on 2021-03-07 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0027_order_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
    ]
