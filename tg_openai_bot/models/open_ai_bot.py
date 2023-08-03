from intagration_utils_candidate.app_telegram_bot.models.abstract_bot import AbstractBot
from tg_openai_bot.models import OpenAiUser, OpenAiUserChat, OpenAiUserMessage


def handle_updates():
    OpenAiBot.objects.get(pk=1).handle_updates()


class OpenAiBot(AbstractBot):
    USER_CLASS = OpenAiUser
    CHAT_CLASS = OpenAiUserChat
    MESSAGE_CLASS = OpenAiUserMessage

    def on_start_command(self, message, t_user, t_chat, param):
        self.send_message(t_chat.telegram_id, "Команда start принята")

    def on_message(self, message, t_user, t_chat):
        self.send_message(t_chat.telegram_id, f"Вы прислали { message }")

    # def on_gpt_command(self, t_chat):
    #
    #     self.send_message(t_chat.telegram_id, context.text)
