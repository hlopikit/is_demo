import openai
from telegram.ext import Updater, CommandHandler, CallbackContext
from django.conf import settings
from integration_utils.vendors.telegram import Bot, Update

MODEL = "gpt-3.5-turbo"


def gpt_handler(update: Update, context: CallbackContext):
    messages = []
    user_input = " ".join(context.args)
    messages.append({"role": "user", "content": user_input})
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages
    )
    response_content = completion.choices[0].message.content

    messages.append({"role": "assistant", "content": response_content})
    update.message.reply_text(response_content)


def load_handler(bot_token, handler_name, handler_func):
    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(f"{handler_name}", handler_func))
    updater.start_polling()
    updater.idle()


#  Регаем бота через токен из view
def register_bot(bot_token):
    bot = Bot(token=bot_token)
    load_handler(bot_token, handler_name='gpt', handler_func=gpt_handler)
    return bot


#  Выводим сообщение о том что бо создан
def say_hello(bot, chat_id):
    bot.send_message(chat_id=chat_id,
                     text='Бот активирован успешно, для того чтобы начать диалог напишите свой '
                          'вопрос после команды /gpt')
