# Generated by Django 5.0.6 on 2024-08-06 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_order_country_order_county_order_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='county',
        ),
    ]
