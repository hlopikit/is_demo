0) pip install python-telegram-bot
1) Скопируйте example_bot как новое приложение
2) замените example в файлах и их названиях на другое имя бота
3) Удалите миграции
4) пропишите в Settings новое приложение
5) makemigration и мигрейт
6) создайте бота в телеграме
7) создайте запись в модели бота указав название и его токен
8) пропишите крон функцию its_utils.app_telegram_bot.cron.handle_bot_updates указав путь к модели бота {"class_path":"partners_bot.models.partners_bot.PartnersBot"}

