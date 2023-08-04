from django.db import models
from django.utils import timezone

# TODO find and import files
# from its_utils.app_admin.json_admin import JsonAdmin
# from its_utils.functions.compatibility import get_json_field

# JSONField = get_json_field()


def voice_upload_path(instance, filename):
    return u'chat/{}/voice/{}'.format(instance.chat.id, filename)


class AbstractMessage(models.Model):
    telegram_id = models.IntegerField()
    chat = models.ForeignKey('telegram_bot.TelegramChat', on_delete=models.CASCADE, related_name='history')
    author = models.ForeignKey('telegram_bot.TelegramUser', on_delete=models.CASCADE, null=True)
    text = models.TextField(default='', null=True)
    date = models.DateTimeField(default=timezone.now)
    voice = models.FileField(upload_to=voice_upload_path, null=True, blank=True)

    caption = models.TextField(default='', null=True)
    # effective_attachment = JSONField(blank=True, null=True)

    def __str__(self):
        return '#{}: {} => chat {} ({})'.format(self.telegram_id, self.author, self.chat.telegram_id, self.date)

    class Meta:
        abstract = True
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    # TODO implement JsonAdmin
    # class Admin(JsonAdmin):
    #     list_display = 'chat', 'author', 'text'
    #     list_display_links = list_display

    def append_text(self, text):
        text = "{}\n{}".format(self.text, text)
        self.edit_message_text(text)

    def edit_message_text(self, text, parse_mode='HTML'):
        self.chat.bot.client.edit_message_text(
            text=text,
            chat_id=self.chat.telegram_id,
            message_id=self.telegram_id,
            parse_mode=parse_mode
        )
        self.text = text
        self.save(update_fields=['text'])
