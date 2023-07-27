from django.db import models

from its_utils.app_telegram_bot.models.abstract_chat import AbstractChat


class HrChat(AbstractChat):
    bot = models.ForeignKey('HrBot', on_delete=models.PROTECT)


