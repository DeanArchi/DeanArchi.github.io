import re
from dotenv import load_dotenv
import os

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import telebot
from telebot import types

from bot.models import TelegramUser, Currency

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
TG_BASE_URL = os.getenv('TG_BASE_URL')

API_KEY = os.getenv('API_KEY')
API_BASE_URL = os.getenv('API_BASE_URL')

bot = telebot.TeleBot(BOT_TOKEN)


@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'Method not allowed'}, status=405)


@bot.message_handler(commands=['help'])
def user_help(message):
    prepared_message = 'Hello! I`m Currency Convert Bot.' \
                       'Here`s the list of commands available for me:\n' \
                       '1. <b><u>Exchange rate</u></b>. Find out the latest exchange rates for different ' \
                       'currencies. I`ll provide you with updated information on exchange rates\n' \
                       '2. <b><u>Currency conversion</u></b>. Enter the amount and currency you need, and ' \
                       'then specify the currency you want to convert to. I`ll provide you with the ' \
                       'exact equivalent in the selected currency.\n' \
                       '3. <b><u>Watchlist</u></b>. Add currency pairs to your watchlist to receive notifications when' \
                       ' the exchange rate changes. You`ll always be up-to-date with the latest changes.\n' \
                       'Type /start to begin work with bot'
    bot.send_message(message.chat.id, prepared_message, parse_mode='html')


@bot.message_handler(commands=['start'])
def start(message):
    try:
        telegram_user = TelegramUser.objects.get(username=message.chat.username, chat_id=message.chat.id)
    except TelegramUser.DoesNotExist:
        telegram_user = TelegramUser(
            username=message.chat.username,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name,
            chat_id=message.chat.id
        )
        telegram_user.save()

    prepared_message = 'Choose operation: '
    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('Exchange rate')
    button2 = types.KeyboardButton('Currency conversion')
    button3 = types.KeyboardButton('Watchlist')
    markup.row(button1)
    markup.row(button2, button3)
    bot.send_message(message.chat.id, prepared_message, reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    match message.text:
        case 'Exchange rate':
            exchange_rate(message)
        case 'Currency conversion':
            currency_conversion(message)
        case 'Watchlist':
            bot.send_message(message.chat.id, 'You chose 3 option')


def get_list_of_currencies(chat_id):
    count = 1
    list_currencies = Currency.objects.all()
    prepared_message = 'List of available currencies:\n'
    for currency in list_currencies:
        prepared_message += f'{count}. {currency}\n'
        count += 1
    bot.send_message(chat_id, prepared_message)


def check_input_data(message):
    data = message.text.strip().upper()
    pattern = re.compile(r'^[A-Z]{3}/[A-Z]{3}$')
    if not pattern.match(data):
        bot.send_message(message.chat.id, 'Write your choice in the form "USD/EUR"')
        bot.register_next_step_handler(message, check_input_data)
    else:
        first_currency, second_currency = data.split('/')
        currency_codes = Currency.objects.values_list('currency_code', flat=True)

        if first_currency not in currency_codes:
            bot.send_message(message.chat.id, f'There`s no {first_currency} in the list above.')
            bot.register_next_step_handler(message, check_input_data)
        elif second_currency not in currency_codes:
            bot.send_message(message.chat.id, f'There`s no {second_currency} in the list above.')
            bot.register_next_step_handler(message, check_input_data)
        elif first_currency == second_currency:
            bot.send_message(message.chat.id, f'You can`t input 2 same currencies.')
            bot.register_next_step_handler(message, check_input_data)
        else:
            get_currencies = requests.get(f'{API_BASE_URL}{API_KEY}/latest/{first_currency}')
            get_currencies_json = get_currencies.json()
            user_data = {
                'first_currency': first_currency,
                'second_currency': second_currency,
                'get_currencies_json': get_currencies_json
            }
            return user_data


def handle_user_choice(message, request_type):
    user_data = check_input_data(message)
    if user_data:
        match request_type:
            case 'exchange_rate':
                get_exchange_rate(message, user_data)
            case 'currency_conversion':
                # user_input_amount_of_money(message, user_data)
                bot.send_message(message.chat.id, 'Enter the amount of money to convert')
                bot.register_next_step_handler(message, lambda msg: user_input_amount_of_money(msg, user_data))
    else:
        bot.register_next_step_handler(message, lambda msg: handle_user_choice(msg, request_type))


def get_exchange_rate(message, user_data):
    first_currency = user_data['first_currency']
    second_currency = user_data['second_currency']
    get_currencies_json = user_data['get_currencies_json']

    conversion_rates = get_currencies_json['conversion_rates']
    chosen_exchange_rate = round(conversion_rates[second_currency], 2)

    prepared_message = f'1 {first_currency} costs {chosen_exchange_rate} {second_currency}'
    bot.send_message(message.chat.id, prepared_message)
    bot.send_message(message.chat.id, 'Type /start to continue work with bot')


def exchange_rate(message):
    request_type = 'exchange_rate'
    get_list_of_currencies(message.chat.id)
    bot.send_message(message.chat.id, 'Write your choice in the form "USD/EUR"')
    bot.register_next_step_handler(message, lambda msg: handle_user_choice(msg, request_type))


def user_input_amount_of_money(message, user_data):
    try:
        user_input = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid input. Please enter a valid numerical amount for conversion')
        bot.register_next_step_handler(message, lambda msg: user_input_amount_of_money(msg, user_data))
    else:
        convert_currency_amount(message, user_data, user_input)


def convert_currency_amount(message, user_data, amount):
    first_currency = user_data['first_currency']
    second_currency = user_data['second_currency']
    get_currencies_json = user_data['get_currencies_json']

    conversion_rates = get_currencies_json["conversion_rates"]
    chosen_exchange_rate = conversion_rates[second_currency]

    converted_amount = round(amount * chosen_exchange_rate, 2)
    prepared_message = f"{amount} {first_currency} costs {converted_amount} {second_currency}"
    bot.send_message(message.chat.id, prepared_message)
    bot.send_message(message.chat.id, 'Type /start to continue work with bot')


def currency_conversion(message):
    request_type = 'currency_conversion'
    get_list_of_currencies(message.chat.id)
    bot.send_message(message.chat.id, 'Write your choice in the form "USD/EUR"')
    bot.register_next_step_handler(message, lambda msg: handle_user_choice(msg, request_type))