from django.contrib import admin
from django.db import models

from its_utils.app_telegram_bot.models.abstract_chat import AbstractChat


class HrCheckpoint(models.Model):
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    user = models.ForeignKey('HrUser', on_delete=models.PROTECT)
    text = models.TextField()

    class Admin(admin.ModelAdmin):
        list_display = ['from_time', 'to_time', 'user', 'text']
        #list_display_links = list_display
        # inlines = ChatParticipantInline,
        #search_fields = 'telegram_id',



