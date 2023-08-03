from django.db import models


# TODO find and import file
# from its_utils.app_admin.json_admin import JsonAdmin


class AbstractChatParticipant(models.Model):
    chat = models.ForeignKey('TelegramChat', related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey('TelegramUser', related_name='participated_chats', on_delete=models.CASCADE)

    class Meta:
        abstract = True
        unique_together = 'chat', 'user'

        verbose_name = 'Участник чата'
        verbose_name_plural = 'Участники чатов'

    # TODO uncomment after JsonAdmin implement
    # class Admin(JsonAdmin):
    #     list_display = 'chat', 'user',
    #     list_display_links = list_display

    def __str__(self):
        return '{}@{}'.format(self.user.username or "user{}".format(self.user.telegram_id), self.chat.telegram_id)
