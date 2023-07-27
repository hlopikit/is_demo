from its_utils.app_telegram_bot.example_bot.models import ExampleUser, ExampleChat, ExampleMessage
from its_utils.app_telegram_bot.models.abstract_bot import AbstractBot

def handle_updates():
    ExampleBot.objects.get(pk=1).handle_updates()


class ExampleBot(AbstractBot):
    USER_CLASS = ExampleUser
    CHAT_CLASS = ExampleChat
    MESSAGE_CLASS = ExampleMessage

    def on_start_command(self, message, t_user, t_chat, param):
        self.send_message(t_chat.telegram_id, "Команда start принята")

