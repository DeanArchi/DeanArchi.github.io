Currency Convert Bot for Telegram

Here's link to landing page of the bot: https://deanarchi.github.io

Installation.
1. Create a bot using BotFather
2. Generate an api key in the service at the link: https://v6.exchangerate-api.com
3.  Clone the repository
4. Install dependencies
5. Set up the configuration: copy `.env.example` to `.env` and change the settings.

Usage.
1. Generate a link using ngrok (ngrok http 8000) and add it to the settings.py file according to the instructions
2. In Postman (or similar), run the command https://api.telegram.org/bot{YOUR_BOT_TOKEN}/setWebhook with the url parameter (for example, "url": "https://fa1f-178-54-136-100.ngrok.io/webhook/")
3. Run redis in docker (docker run --name redis-container-name -p 6379:6379 redis)
4. Run celery (celery --app currency_bot worker)
5. Run the project (python manage.py runserver)
