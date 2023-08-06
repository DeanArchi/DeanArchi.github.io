from django.db import models


class Currency(models.Model):
    currency_name = models.CharField(max_length=50, blank=False, null=False)
    currency_code = models.CharField(max_length=3, blank=False, null=False)

    def __str__(self):
        return f'{self.currency_name} - {self.currency_code}'

    class Meta:
        db_table = 'currency'
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class TelegramUser(models.Model):
    chat_id = models.IntegerField(blank=False, null=False, default=0)
    username = models.CharField(max_length=50, blank=False, null=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.username}; id {self.chat_id}; {self.first_name} {self.last_name}'

    class Meta:
        db_table = 'telegram_user'
        verbose_name = 'Telegram user'
        verbose_name_plural = 'Telegram users'

