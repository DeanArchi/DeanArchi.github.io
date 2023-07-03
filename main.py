import requests

API_KEY = "secret_key"

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
            return f"You can only input numbers from 1 to {len(currencies_list)}"

        chosen_currency_1 = currency_values[user_chosen_currency_1 - 1]
        chosen_currency_2 = currency_values[user_chosen_currency_2 - 1]

        get_currencies = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{chosen_currency_1}")
        get_currencies_json = get_currencies.json()
        return chosen_currency_1, chosen_currency_2, get_currencies_json
    except ValueError:
        return "Wrong value, you can input only numbers"


def get_exchange_rate():
    currency_1, currency_2, get_currencies_json = get_currency_response()

    conversion_rates = get_currencies_json["conversion_rates"]
    chosen_currency_rate = conversion_rates[currency_2]

    return f"1 {currency_1} costs {chosen_currency_rate} {currency_2}"


def convert_currency_amount():
    currency_1, currency_2, get_currencies_json = get_currency_response()

    try:
        user_amount_of_money = float(input("Enter the amount of money to convert: "))
    except ValueError:
        return "Wrong value, you can input only numbers"

    conversion_rates = get_currencies_json["conversion_rates"]
    currency_rate_2 = conversion_rates[currency_2]

    calculated_result = round(user_amount_of_money * currency_rate_2, 2)
    return f"{user_amount_of_money} {currency_1} costs {calculated_result} {currency_2}"


# print(get_exchange_rate())
print(convert_currency_amount())
