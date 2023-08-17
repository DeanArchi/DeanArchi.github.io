from celery import shared_task
import os
import requests
from dotenv import load_dotenv
import telebot

from bot.models import UserWatchlist

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('API_KEY')
API_BASE_URL = os.getenv('API_BASE_URL')

bot = telebot.TeleBot(BOT_TOKEN)


@shared_task
def check_watchlist_updates():
    watchlist = UserWatchlist.objects.all()
    for currency_pair in watchlist:
        first_currency = currency_pair.first_currency.currency_code
        second_currency = currency_pair.second_currency.currency_code

        get_currencies = requests.get(f'{API_BASE_URL}{API_KEY}/latest/{first_currency}')
        get_currencies_json = get_currencies.json()

        conversion_rates = get_currencies_json["conversion_rates"]
        exchange_rate_checked = round(conversion_rates[second_currency], 2)

        if exchange_rate_checked != currency_pair.exchange_rate:
            pair = UserWatchlist.objects.get(id=currency_pair.id)
            pair.exchange_rate = exchange_rate_checked
            pair.save(update_fields=['exchange_rate'])

            prepared_message = (f'There are changes in pair`s {first_currency} - {second_currency}.\n'
                                f'New exchange rate: {exchange_rate_checked}')
            bot.send_message(currency_pair.user.chat_id, prepared_message)
