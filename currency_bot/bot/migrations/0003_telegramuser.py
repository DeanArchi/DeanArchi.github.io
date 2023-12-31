# Generated by Django 4.2.3 on 2023-07-28 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_alter_currency_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Telegram user',
                'verbose_name_plural': 'Telegram users',
                'db_table': 'telegram_user',
            },
        ),
    ]
