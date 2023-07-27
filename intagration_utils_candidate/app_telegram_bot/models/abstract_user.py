from django.db import models
from django.contrib import admin


class AbstractUser(models.Model):
    telegram_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100, default='', blank=True, null=True)
    first_name = models.CharField(max_length=127, default='', blank=True, null=True)
    last_name = models.CharField(max_length=127, default='', blank=True, null=True)

    class Meta:
        abstract = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return "{} {}".format(
            self.first_name, self.last_name
        ).strip() or self.username or "user{}".format(
            self.telegram_id
        )

    class Admin(admin.ModelAdmin):
        list_display = 'telegram_id', 'username', 'first_name', 'last_name'
        list_display_links = list_display

    @classmethod
    def from_update(cls, update):
        if update.message:
            from_user = update.message.from_user

        elif update.callback_query:
            from_user = update.callback_query.from_user

        elif update.inline_query:
            from_user = update.inline_query.from_user

        elif update.edited_message:
            from_user = update.edited_message.from_user

        elif update.chat_join_request:
            from_user = update.chat_join_request.from_user

        else:
            return None

        user, _ = cls.objects.get_or_create(telegram_id=from_user.id)
        user.username = from_user.username
        user.first_name = from_user.first_name
        user.last_name = from_user.last_name
        user.save(update_fields=['username', 'first_name', 'last_name'])

        return user
