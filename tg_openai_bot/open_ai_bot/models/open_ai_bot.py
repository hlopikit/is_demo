from tg_openai_bot.open_ai_bot.models import open_ai_user, open_ai_chat, open_ai_message
from intagration_utils_candidate.app_telegram_bot.models.abstract_bot import AbstractBot


def handle_updates():
    OpenAiBot.objects.get(pk=1).handle_updates()


class OpenAiBot(AbstractBot):
    USER_CLASS = open_ai_user.OpenAiUser
    CHAT_CLASS = open_ai_chat.OpenAiUserChat
    MESSAGE_CLASS = open_ai_message.OpenAiUserMessage

    def on_start_command(self, message, t_user, t_chat, param):
        self.send_message(t_chat.telegram_id, "Команда start принята")


    # def on_gpt_command(self, t_chat):
    #
    #     self.send_message(t_chat.telegram_id, context.text)
