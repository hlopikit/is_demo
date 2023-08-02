import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from django.conf import settings
from integration_utils.vendors.telegram import Bot

MODEL = "gpt-3.5-turbo"
openai.api_key = settings.OPEN_AI_API_KEY

# Список команд доступных боту
VALID_BOT_COMMANDS = ["gpt", "help"]


def gpt_handler(update, context):
    # Создаем или получаем историю диалога пользователя из контекста
    context.user_data.setdefault("dialog_history", [])
    messages = context.user_data["dialog_history"]

    # Получаем ввод пользователя и добавляем его в историю диалога
    user_input = " ".join(context.args)
    messages.append({"role": "user", "content": user_input})

    # Генерируем ответ с помощью GPT-3.5
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages
    )
    response_content = completion.choices[0].message.content

    # Добавляем ответ в историю диалога
    messages.append({"role": "assistant", "content": response_content})
    context.user_data["dialog_history"] = messages

    # Отправляем ответ пользователю
    update.message.reply_text(response_content)


def help_handler(update, context):
    update.message.reply_text(f'Список доступных на данный момент команд - {", ".join(str(x) for x in VALID_BOT_COMMANDS)}')


def is_valid_command(command):
    # Проверяем, является ли команда допустимой
    return command in VALID_BOT_COMMANDS


def unknown_command(update, context):
    # Обрабатываем неизвестные команды
    update.message.reply_text('Извините, такой команды не существует.')


def register_bot(bot_token):
    # Регистрируем бота с помощью токена из BotFather
    bot = Bot(token=bot_token)
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher

    # Регистрируем обработчик для команды /gpt
    dispatcher.add_handler(CommandHandler("gpt", gpt_handler))

    # Регистрируем обработчик для команды /help
    dispatcher.add_handler(CommandHandler("help", help_handler))

    # Регистрируем обработчик для неизвестных команд
    dispatcher.add_handler(MessageHandler(Filters.command & ~Filters.update.edited_message, handle_unknown_command))

    # Запускаем бота
    updater.start_polling()
    return bot


def handle_unknown_command(update, context):
    # Проверяем, является ли команда неизвестной и отвечаем соответствующим сообщением
    command = update.message.text.split()[0].lower()

    if not is_valid_command(command):
        unknown_command(update, context)


def say_hello(bot, chat_id):
    # Отправляем приветственное сообщение о том, что бот активирован
    bot.send_message(chat_id=chat_id,
                     text='Бот активирован успешно, для того чтобы начать диалог напишите свой '
                          'вопрос после команды /gpt')
