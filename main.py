import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

currencies_list = {
    "United States Dollar": "USD",
    "Euro": "EUR",
    "Ukrainian Hryvnia": "UAH",
    "Czech Koruna": "CZK",
    "Swiss Franc": "CHF"
}


def get_currency_response():
    count = 1
    for currency in currencies_list.keys():
        print(f"{count}. {currency}")
        count += 1

    try:
        user_chosen_currency_1 = int(input("Choose 1 currency from the list: "))
        user_chosen_currency_2 = int(input("Choose 2 currency from the list: "))

        currency_values = list(currencies_list.values())

        if user_chosen_currency_1 > len(currencies_list) or user_chosen_currency_1 < 1 \
                or user_chosen_currency_2 > len(currencies_list) or user_chosen_currency_2 < 1:
            # return f"You can only input numbers from 1 to {len(currencies_list)}"
            return None, None, None

        chosen_currency_1 = currency_values[user_chosen_currency_1 - 1]
        chosen_currency_2 = currency_values[user_chosen_currency_2 - 1]

        get_currencies = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{chosen_currency_1}")
        get_currencies_json = get_currencies.json()
        return chosen_currency_1, chosen_currency_2, get_currencies_json
    except ValueError:
        # return "Wrong value, you can input only numbers"
        return None, None, None


def check_response(currency_1, currency_2, get_currencies_json):
    if currency_1 is None or currency_2 is None or get_currencies_json is None:
        return f"You can only input numbers from 1 to {len(currencies_list)}"


def get_exchange_rate():
    currency_1, currency_2, get_currencies_json = get_currency_response()

    error_message = check_response(currency_1, currency_2, get_currencies_json)
    if error_message:
        return error_message

    conversion_rates = get_currencies_json["conversion_rates"]
    chosen_currency_rate = conversion_rates[currency_2]

    return f"1 {currency_1} costs {chosen_currency_rate} {currency_2}"


def convert_currency_amount():
    currency_1, currency_2, get_currencies_json = get_currency_response()

    error_message = check_response(currency_1, currency_2, get_currencies_json)
    if error_message:
        return error_message

    try:
        user_amount_of_money = float(input("Enter the amount of money to convert: "))
    except ValueError:
        return "Wrong value, you can input only numbers"

    conversion_rates = get_currencies_json["conversion_rates"]
    currency_rate_2 = conversion_rates[currency_2]

    calculated_result = round(user_amount_of_money * currency_rate_2, 2)
    return f"{user_amount_of_money} {currency_1} costs {calculated_result} {currency_2}"


def add_to_watchlist(watchlist):
    currency_1, currency_2, get_currencies_json = get_currency_response()

    error_message = check_response(currency_1, currency_2, get_currencies_json)
    if error_message:
        return error_message

    for key in watchlist.keys():
        if (currency_1, currency_2) == key:
            return f"Currency pair {currency_1} - {currency_2} is already in your watchlist."
    else:
        conversion_rate = get_currencies_json["conversion_rates"][currency_2]
        watchlist[(currency_1, currency_2)] = conversion_rate
        return f"Added {currency_1} to {currency_2} to your watchlist."


def delete_from_watchlist(watchlist):
    for index, (currencies, rates) in enumerate(watchlist.items(), start=1):
        print(f"{index}. {currencies} - {rates}")

    choice_for_deleting = input("Choose currency pair you want to delete: ")

    try:
        choice_for_deleting = int(choice_for_deleting)
    except ValueError:
        return "Wrong value, you can input only numbers"

    if choice_for_deleting < 1 or choice_for_deleting > len(watchlist):
        return f"You can input only numbers from 1 to {len(watchlist)}"

    count = 1
    selected_pair = None

    for currencies, rates in watchlist.items():
        if count == choice_for_deleting:
            selected_pair = currencies
            del watchlist[currencies]
            break
        count += 1

    return f"Deleted {selected_pair} from your watchlist."


def send_notification(currencies, rates):
    return f"There's changes in the {currencies[0]} - {currencies[1]} exchange rate.\n" \
           f"Old exchange rate: {rates[0]}\n" \
           f"New exchange rate: {rates[1]}\n"


def check_watchlist(watchlist):
    print("\nChecking your watchlist...\n")

    changes_in_currency_rate = {}
    is_changes_detected = False

    if watchlist:
        for currencies, rate in watchlist.items():
            get_currencies = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{currencies[0]}")
            get_currencies_json = get_currencies.json()
            conversion_rate = get_currencies_json["conversion_rates"][currencies[1]]

            if watchlist[currencies] != conversion_rate:
                changes_in_currency_rate[currencies] = (watchlist[currencies], conversion_rate)
                watchlist[currencies] = conversion_rate
                is_changes_detected = True

        for currencies, rates in changes_in_currency_rate.items():
            print(send_notification(currencies, rates))

        if not is_changes_detected:
            return "Nothing has changed."
        else:
            return "Watchlist updated successfully."
    else:
        return "Your watchlist is empty."


# ==== This line of code is needed to check whether the notification of changes
# ==== in the exchange rate that have been added to the watchlist is sent
user_watchlist = {('USD', 'UAH'): 9, ('EUR', 'UAH'): 8}
# user_watchlist = {}
while True:
    print("\nSelect an option:")
    print("1. Convert currency amount")
    print("2. Get exchange rate")
    print("3. Add currency pair to watchlist")
    print("4. Delete currency pair from watchlist")
    print("5. Check your watchlist")
    print("6. Check for changes in the watchlist")
    print("7. Exit")

    user_choice = input("Choose operation: ")
    try:
        user_choice = int(user_choice)
    except ValueError:
        print("Input only numbers")
    else:
        match user_choice:
            case 1:
                print(convert_currency_amount())
            case 2:
                print(get_exchange_rate())
            case 3:
                print(add_to_watchlist(user_watchlist))
            case 4:
                print(delete_from_watchlist(user_watchlist))
            case 5:
                print(user_watchlist)
            case 6:
                print(check_watchlist(user_watchlist))
            case 7:
                break
            case _:
                print("Unknown command")
