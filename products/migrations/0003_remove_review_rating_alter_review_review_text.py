# Generated by Django 5.0.6 on 2024-07-12 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_customer_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        migrations.AlterField(
            model_name='review',
            name='review_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]