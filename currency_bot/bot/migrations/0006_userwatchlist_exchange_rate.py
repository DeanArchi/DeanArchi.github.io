# Generated by Django 4.2.3 on 2023-08-08 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_userwatchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwatchlist',
            name='exchange_rate',
            field=models.FloatField(default=0),
        ),
    ]