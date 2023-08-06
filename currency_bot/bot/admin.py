from django.contrib import admin
from bot.models import Currency, TelegramUser


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    pass
