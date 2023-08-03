from django.db import models

from intagration_utils_candidate.app_telegram_bot.models.abstract_message import AbstractMessage


class OpenAiUserMessage(AbstractMessage):
    chat = models.ForeignKey('OpenAiUserChat', on_delete=models.CASCADE, related_name='history')
    author = models.ForeignKey('OpenAiUser', on_delete=models.CASCADE, null=True)
