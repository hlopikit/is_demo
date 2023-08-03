from django.db import models

from intagration_utils_candidate.app_telegram_bot.models.abstract_chat import AbstractChat


class OpenAiUserChat(AbstractChat):
    bot = models.ForeignKey('OpenAiBot', on_delete=models.PROTECT)


