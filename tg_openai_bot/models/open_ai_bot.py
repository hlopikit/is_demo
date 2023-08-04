from django.conf import settings

from intagration_utils_candidate.app_telegram_bot.models.abstract_bot import AbstractBot
from tg_openai_bot.models import OpenAiUser, OpenAiUserChat, OpenAiUserMessage

import openai
openai.api_key = settings.OPEN_AI_API_KEY

MODEL = "gpt-3.5-turbo"


def handle_updates():
    OpenAiBot.objects.get(pk=1).handle_updates()


class OpenAiBot(AbstractBot):
    USER_CLASS = OpenAiUser
    CHAT_CLASS = OpenAiUserChat
    MESSAGE_CLASS = OpenAiUserMessage
    CONTEXT = []
    VALID_COMMAND = ['/start', '/gpt']

    def on_start_command(self, message, t_user, t_chat, param):
        self.send_message(t_chat.telegram_id, "Команда start принята, чтобы спросить бота, напишите /gpt")

    def on_gpt_command(self, message, t_user, t_chat, param):
        if not param:
            self.send_message(t_chat.telegram_id, 'Введите запрос')
            return
        OpenAiBot.CONTEXT.append({'role': 'user', 'content': param})
        completion = openai.ChatCompletion.create(
            model=MODEL,
            messages=OpenAiBot.CONTEXT
        )
        response_content = completion.choices[0].message.content
        self.send_message(t_chat.telegram_id, response_content)
        OpenAiBot.CONTEXT.append({'role': 'assistant', 'content': response_content})

    def on_help_command(self, message, t_user, t_chat, param):
        self.send_message(t_chat.telegram_id, "На данный момент доступны следующие команды:\n"
                                              "/start - проверка бота\n"
                                              "/gpt - задать вопрос")

