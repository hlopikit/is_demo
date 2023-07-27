from django.db import models
from django.utils.crypto import get_random_string
from django.contrib import admin


class AbstractChat(models.Model):
    TYPE_PRIVATE = 'private'
    TYPE_GROUP = 'group'
    TYPE_SUPERGROUP = 'supergroup'
    TELEGRAM_TYPE_CHOICES = (
        (TYPE_PRIVATE, TYPE_PRIVATE),
        (TYPE_GROUP, TYPE_GROUP),
        (TYPE_SUPERGROUP, TYPE_SUPERGROUP)
    )

    class Meta:
        abstract = True
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    telegram_id = models.CharField(max_length=100)
    telegram_type = models.CharField(max_length=25, default='', null=True, blank=True, choices=TELEGRAM_TYPE_CHOICES)
    bot = models.ForeignKey('TelegramBot', on_delete=models.PROTECT)

    secret = models.CharField(max_length=50, default='', blank=True)

    def __str__(self):
        return 'chat{}'.format(self.telegram_id)

    def get_secret(self):
        if not self.secret:
            self.secret = get_random_string(20)
            self.save(update_fields=['secret'])

        return self.secret

    def get_link(self):
        return 'https://web.telegram.org/#/im?p=g{}'.format(self.telegram_id)

    class Admin(admin.ModelAdmin):
        list_display = 'telegram_id',
        list_display_links = list_display
        # inlines = ChatParticipantInline,
        search_fields = 'telegram_id',

    @classmethod
    def from_update(cls, update, bot):
        if update.message:
            chat_id = update.message.chat_id
            chat_type = update.message.chat.type

        elif update.callback_query:
            chat_id = update.callback_query.message.chat_id
            chat_type = update.callback_query.message.chat.type

        elif update.edited_message:
            chat_id = update.edited_message.chat_id
            chat_type = update.edited_message.chat.type

        elif update.chat_join_request:
            chat_id = update.chat_join_request.chat.id
            chat_type = update.chat_join_request.chat.type

        else:
            return None

        chat, _ = cls.objects.get_or_create(telegram_id=chat_id, defaults=dict(bot=bot))
        chat.bot = bot
        chat.telegram_type = chat_type
        chat.save(update_fields=['bot', 'telegram_type'])

        return chat
