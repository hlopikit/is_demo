import openai
from telegram.ext import Updater, CommandHandler, CallbackContext
from django.conf import settings
from integration_utils.vendors.telegram import Bot, Update

MODEL = "gpt-3.5-turbo"
openai.api_key = settings.OPEN_AI_API_KEY


def gpt_handler(update: Update, context: CallbackContext):
    context.user_data.setdefault("dialog_history", [])
    messages = context.user_data["dialog_history"]
    user_input = " ".join(context.args)
    messages.append({"role": "user", "content": user_input})
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages
    )
    response_content = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response_content})
    context.user_data["dialog_history"] = messages
    update.message.reply_text(response_content)


#  TODO make useful func for searching non-existing commands
def unknown_command(update, context):
    command = update.message.text.split()[0]  # Получаем первое слово из сообщения (должно быть командой)
    if command.startswith('/'):
        command = command[1:]  # Убираем символ '/' в начале команды
        if not context.bot.get_command(command):
            update.message.reply_text('Извините, такой команды не существует.')
    else:
        update.message.reply_text('Извините, я не понимаю эту команду.')


def load_handlers(bot_token, handler_name, handler_func):
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(f"{handler_name}", handler_func))
    dispatcher.add_handler(CommandHandler('unknown', unknown_command))
    updater.start_polling()


#  Регаем бота через токен из view
def register_bot(bot_token):
    bot = Bot(token=bot_token)
    load_handlers(bot_token, 'gpt', gpt_handler)
    return bot


#  Выводим сообщение о том что бо создан
def say_hello(bot, chat_id):
    bot.send_message(chat_id=chat_id,
                     text='Бот активирован успешно, для того чтобы начать диалог напишите свой '
                          'вопрос после команды /gpt')
