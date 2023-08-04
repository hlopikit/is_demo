from django.db import models

from intagration_utils_candidate.app_telegram_bot.models.abstract_chat_participant import AbstractChatParticipant


class OpenAiChatParticipant(AbstractChatParticipant):
    chat = models.ForeignKey('OpenAiUserChat', related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey('OpenAiUser', related_name='participated_chats', on_delete=models.CASCADE)


