from django.db import models

from its_utils.app_telegram_bot.models.abstract_chat_participant import AbstractChatParticipant


class HrChatParticipant(AbstractChatParticipant):
    chat = models.ForeignKey('HrChat', related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey('HrUser', related_name='participated_chats', on_delete=models.CASCADE)


