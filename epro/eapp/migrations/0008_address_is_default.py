# Generated by Django 5.2 on 2025-05-05 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eapp', '0007_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]
