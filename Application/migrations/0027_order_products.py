# Generated by Django 3.1.2 on 2021-03-07 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0026_order_cort'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Application.cartproduct'),
        ),
    ]