from django.db import models

from intagration_utils_candidate.app_telegram_bot.models.abstract_chat_participant import AbstractChatParticipant


class ExampleChatParticipant(AbstractChatParticipant):
    chat = models.ForeignKey('ExampleChat', related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey('ExampleUser', related_name='participated_chats', on_delete=models.CASCADE)


