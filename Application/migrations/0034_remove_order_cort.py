# Generated by Django 3.1.2 on 2021-03-12 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0033_auto_20210312_1005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cort',
        ),
    ]