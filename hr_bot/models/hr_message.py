from django.db import models

from its_utils.app_telegram_bot.models.abstract_message import AbstractMessage


class HrMessage(AbstractMessage):
    chat = models.ForeignKey('HrChat', on_delete=models.CASCADE, related_name='history')
    author = models.ForeignKey('HrUser', on_delete=models.CASCADE, null=True)


