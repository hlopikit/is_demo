# coding: utf-8
from typing import List
from io import BytesIO


from django.contrib import admin
from django.db import models


from intagration_utils_candidate.app_telegram_bot.common import get_command_from_message, escape_disallowed_tags
from integration_utils.vendors import telegram
from integration_utils.vendors.telegram import Bot
from integration_utils.vendors.telegram.error import TimedOut, BadRequest, Unauthorized, RetryAfter, ChatMigrated
from settings import ilogger


class AbstractBot(models.Model):
    HTML_PARSE_MODE = 'HTML'
    MARKDOWN_PARSE_MODE = 'Markdown'

    NO_CHANGES_ERROR_MESSAGE = 'exactly the same as a current'
    MAX_MESSAGE_LENGTH = 4096

    USER_CLASS = None
    CHAT_CLASS = None
    MESSAGE_CLASS = None

    TELEGRAM_API_BASE_URL = 'https://api.telegram.org/bot'
    # Если хотим через наш сервак то переопределить
    # TELEGRAM_API_BASE_URL = 'https://telegram-client.it-solution.ru/tapi/bot'

    TELEGRAM_API_PROXY = None

    RAISE_CHAT_MIGRATED_ERROR = False
    RAISE_UNAUTHORIZED_ERROR = False
    CHECK_SAFE_ERROR_FUNC = None

    COMMAND_FUNCTIONS_PATH = ''

    GET_UPDATES_TIMEOUT = 5
    ALLOWED_UPDATES = [
        'message', 'inline_query', 'chosen_inline_result', 'callback_query', 'shipping_query', 'pre_checkout_query',
        'chat_join_request'
    ]

    username = models.CharField(max_length=100, default='')
    auth_token = models.CharField(max_length=100, default='')
    last_update_id = models.IntegerField(default=0, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True

    class Admin(admin.ModelAdmin):
        list_display = 'username', 'is_active'
        list_display_links = list_display

    def __init__(self, *args, **kwargs):
        super(AbstractBot, self).__init__(*args, **kwargs)
        self._client = None

    def __str__(self):
        return self.username

    class HandledUpdate:
        def __init__(
                self, t_user, t_chat, update, is_message=False, is_command=False, is_voice=False, is_callback=False,
                is_photo=False, is_document=False, is_chat_migration=False
        ):
            """
            :param t_user: полльзователь (TelegramUser)
            :param t_chat: чат (TelegramChat)
            :param update: обновление
            :param is_message: True, если это сообщение
            :param is_command: True, если это команда
            :param is_voice:  True, если это голосовое сообщение
            :param is_callback:  True, если это нажатие на кнопку клавиатуры
            :param is_photo:  True, если это фото
            :param is_document:  True, если это файл
            :param is_chat_migration:  True, если это событие миграции чата
            """

            self.t_user = t_user
            self.t_chat = t_chat
            self.update = update
            self.is_message = is_message
            self.is_command = is_command
            self.is_voice = is_voice
            self.is_callback = is_callback
            self.is_photo = is_photo
            self.is_document = is_document,
            self.is_chat_migration = is_chat_migration

    @property
    def client(self):
        """
        Получить клиент для запросов к api

        :return: объект  telegram.Bot
        """

        if self._client is None:
            from django.conf import settings

            request = None
            if self.TELEGRAM_API_PROXY:
                from integration_utils.vendors.telegram.utils.request import Request
                request = Request(proxy_url=self.TELEGRAM_API_PROXY)

            self._client = Bot(self.auth_token, base_url=self.TELEGRAM_API_BASE_URL, request=request)

        return self._client

    def get_command(self, command, detailed_result=False):
        import importlib

        command_exists = False
        command_is_class_method = True

        # ищем команду в отдельном файле
        if self.COMMAND_FUNCTIONS_PATH:
            try:
                command_module = importlib.import_module(self.COMMAND_FUNCTIONS_PATH)
                handler = getattr(command_module, 'on_{}_command'.format(command[1:]))
                command_is_class_method = False
            except (ImportError, AttributeError):
                handler = None
        else:
            handler = None

        # ищем команду в методах класса
        if handler is None:
            try:
                handler = self.__getattribute__('on_{}_command'.format(command[1:]))
            except AttributeError:
                handler = None

        if handler is not None:
            command_exists = True

        if detailed_result:
            return command_exists, handler, command_is_class_method
        else:
            return command_exists

    def get_updates(self):
        return self.client.get_updates(
            offset=self.last_update_id + 1,
            allowed_updates=self.ALLOWED_UPDATES,
            timeout=self.GET_UPDATES_TIMEOUT,
        )

    def handle_updates(self, fail_silently=False):
        """
        Получить обновления и обработать

        :return: кортеж - количество обновлений, обработанных команд, необработанных команд
        """

        try:
            updates = self.get_updates()
            if updates:
                ilogger.debug('telegram_updates', '{}'.format(updates), log_to_cron=True)
        except TimedOut:
            ilogger.warning('handle_updates_timed_out', '{} handle_updates_timed_out'.format(self), log_to_cron=True)
            return 0, 0, 0
        except telegram.error.Conflict as e:
            ilogger.warning('handle_updates_conflict', '{} use deleteWebhook to delete the webhook first'.format(self),
                            log_to_cron=True)
            if fail_silently:
                return 0, 0, 0
            raise e
        except telegram.error.Unauthorized as e:
            ilogger.warning('handle_updates_unauthorized', '{} Unauthorized'.format(self), log_to_cron=True)
            if fail_silently:
                return 0, 0, 0
            raise e

        handled_updates = []
        commands_handled = commands_failed = 0
        last_update = 0
        for up in updates:
            ilogger.info('tg_bot_event', '{}'.format(str(up)), log_to_cron=True)

            if up.update_id > last_update:
                last_update = up.update_id

            chat_join_request = getattr(up, 'chat_join_request', None)
            if not (up.message or up.callback_query or up.inline_query or up.edited_message or chat_join_request):
                continue

            t_user = self.USER_CLASS.from_update(up)

            if up.inline_query:
                self.on_inline_query(up.inline_query, t_user)
                continue

            t_chat = self.CHAT_CLASS.from_update(up, self)
            t_chat.participants.get_or_create(user=t_user)

            handled_update = self.HandledUpdate(t_user, t_chat, up)
            if up.message:
                if up.message.text is not None:
                    command, param = get_command_from_message(up.message, self.username, bot_to_check=self)
                    if command:
                        if self.on_command(up.message, t_user, t_chat, command, param):
                            commands_handled += 1

                        else:
                            commands_failed += 1

                        handled_update.is_command = True

                    else:
                        self.on_message(up.message, t_user, t_chat)

                        handled_update.is_message = True

                elif up.message.voice:
                    self.on_voice_message(up.message, t_user, t_chat)

                    handled_update.is_voice = True

                elif up.message.photo:
                    self.on_photo(up.message, t_user, t_chat)

                    handled_update.is_photo = True

                elif up.message.document:
                    self.on_document(up.message, t_user, t_chat)

                    handled_update.is_document = True

                elif up.message.migrate_to_chat_id:
                    self.on_chat_migration(up.message, t_user, t_chat)

                    handled_update.is_chat_migration = True

                elif up.message.left_chat_member:
                    left_member = up.message.left_chat_member
                    if left_member.is_bot and left_member.username == self.username:
                        self.on_kick(up.message, t_user, t_chat)

                else:
                    self.on_unidentified_message_type(up.message, t_user, t_chat)

            elif up.edited_message:
                self.on_edited_message(up.edited_message, t_user, t_chat)

            elif chat_join_request:
                self.on_chat_join_request(up.chat_join_request, t_user, t_chat)

            else:
                self.on_query_callback(up.callback_query, t_user, t_chat)

                handled_update.is_callback = True

            handled_updates.append(handled_update)

        if last_update:
            self.last_update_id = last_update
            self.save(update_fields=['last_update_id'])

        self.after_updates_handle(handled_updates)

        return len(handled_updates), commands_handled, commands_failed

    def skip_updates(self):
        """
        Пропустить все текущие обновления
        """

        updates = self.client.get_updates(offset=self.last_update_id + 1, allowed_updates=['message'], timeout=1)
        updates_count = len(updates)
        if updates_count:
            self.last_update_id = max([up.update_id for up in updates])
            self.save(update_fields=['last_update_id'])

        return updates_count

    def on_message(self, message, t_user, t_chat):
        """
        Обработка нового сообщения

        Создать сообщение в базе

        :param message: объект telegram-сообщения
        :param t_user: пользователь telegram
        :param t_chat: чат telegram
        :return: True при успешной обработке
        """

        pass

    def on_command(self, message, t_user, t_chat, command, param):
        """
        Обработака события получения команды

        Находит метод с именем on_{command}_command, вызывает его, предавая параметры:
        message, t_user, t_chat, command, param

        :param message: объект telegram-сообщения
        :param t_user: пользователь telegram
        :param t_chat: чат telegram
        :param command: команда (включая символ '/')
        :param param: параметр

        :return: True при успешной обработке
        """

        command_exists, handler, command_is_class_method = self.get_command(command, detailed_result=True)

        try:
            if command_is_class_method:
                # нашли команду как метод класса бота
                handler(message, t_user, t_chat, param)
            else:
                # нашли команду в отдельном файле в папке self.COMMAND_FUNCTIONS_PATH
                handler(self, message, t_user, t_chat, param)

        except Exception as exc:
            ilogger.error('telegram_command_error', 'bot id: {}; exception: {}'.format(self.id, exc))
            return False

        return True

    def on_query_callback(self, callback_query, t_user, t_chat):
        data = callback_query.data

        if isinstance(data, str) and data.startswith('/'):
            split = data.split(' ', maxsplit=1)
            command, param = split if len(split) == 2 else (split[0], '')
            try:
                return self.on_command(callback_query.message, t_user, t_chat, command, param)

            except Exception as exc:
                ilogger.error('telegram_command_error', 'bot id: {}; exception: {}'.format(self.id, exc))
                return False

        return True

    def on_edited_message(self, message, t_user, t_chat):
        """
        Обработка редактирования сообщения

        :param message: объект telegram-сообщения
        :param t_user: пользователь telegram
        :param t_chat: чат telegram
        :return: True при успешной обработке
        """

        return True

    def on_chat_join_request(self, chat_join_request, t_user, t_chat):
        return True

    def on_voice_message(self, message, t_user, t_chat):
        return True

    def on_photo(self, message, t_user, t_chat):
        return True

    def on_document(self, message, t_user, t_chat):
        return True

    def on_chat_migration(self, message, t_user, t_chat):
        return True

    def on_unidentified_message_type(self, message, t_user, t_chat):
        return True

    def on_inline_query(self, query, t_user):
        pass

    def on_kick(self, message, t_user, t_chat):
        pass

    def send(self, send_type, chat_id, text, pinned=False, parse_mode=None, reply_markup=None, reply_to_message_id=None,
             disable_notification=False, fail_silently=False, api_kwargs=None):

        assert send_type == 'message', "Другие типы не готовы"

        if len(text) > self.MAX_MESSAGE_LENGTH:
            text = 'truncated {}...'.format(text[:self.MAX_MESSAGE_LENGTH - 13])

        if parse_mode == self.HTML_PARSE_MODE:
            try:
                text = escape_disallowed_tags(text)
            except Exception as exc:
                ilogger.warning('telegram_bot_html_escape_error', '[{}] {}\n{}'.format(type(exc).__name__, exc, text))

        try:
            res = self.client.send_message(
                chat_id, text,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                reply_to_message_id=reply_to_message_id,
                disable_notification=disable_notification,
                api_kwargs=api_kwargs
            )
            if pinned:
                self.client.pin_chat_message(chat_id, res.message_id)

            return self.MESSAGE_CLASS(
                telegram_id=res.message_id,
                chat=self.CHAT_CLASS.objects.get(telegram_id=chat_id),
                text=text,
            )
        except BadRequest as e:
            if e.message.startswith("Can't parse entities") and parse_mode != 'Markdown':
                # Рекурсивно вызовем
                return self.send(send_type=send_type,
                                 chat_id=chat_id,
                                 text=text,
                                 pinned=pinned,
                                 parse_mode='Markdown',
                                 reply_markup=reply_markup,
                                 reply_to_message_id=reply_to_message_id,
                                 disable_notification=disable_notification,
                                 fail_silently=False,
                                 api_kwargs=api_kwargs)
            else:
                if e.message == 'Chat not found':
                    ilogger.warning(
                        'telegram_bad_request',
                        'failed to send message (chat_id=%s, bot_id=%s): %s' % (chat_id, self.id, e.message)
                    )
                else:
                    ilogger.error(
                        'telegram_bad_request',
                        'failed to send message (chat_id=%s, bot_id=%s): %s' % (chat_id, self.id, e.message)
                    )
        except Unauthorized as e:
            if e.message == 'Forbidden: bot was kicked from the group chat':
                ilogger.warning('bot_was_kicked',
                                'failed to send message (chat_id=%s, bot_id=%s): %s' % (chat_id, self.id, e))
            else:
                ilogger.warning('telegram_bot_uauthorized',
                                'failed to send message (chat_id=%s, bot_id=%s): %s' % (chat_id, self.id, e))
            if self.RAISE_UNAUTHORIZED_ERROR:
                raise
        except RetryAfter:
            ilogger.warning('telegram_bot_retryafter', 'failed to send message')
        except TimedOut:
            ilogger.warning('telegram_bot_TimedOut', 'failed to send message')
        except ChatMigrated as exc:
            ilogger.warning('telegram_bot_ChatMigrated', 'chat migrated {} => {}'.format(chat_id, exc.new_chat_id))
            return self.send(send_type=send_type,
                             chat_id=exc.new_chat_id,
                             text=text,
                             pinned=pinned,
                             parse_mode=parse_mode,
                             reply_markup=reply_markup,
                             reply_to_message_id=reply_to_message_id,
                             disable_notification=disable_notification,
                             fail_silently=False,
                             api_kwargs=api_kwargs)
        except Exception as exc:
            error_log_message = 'telegram_bot_error=> failed to send message (chat_id=%s, bot_id=%s): %s' % (
                chat_id, self.id, exc)
            if self.CHECK_SAFE_ERROR_FUNC is not None and self.CHECK_SAFE_ERROR_FUNC(exc):
                ilogger.warning(error_log_message)
            else:
                ilogger.error(error_log_message)

        return False

    def send_message(
            self, chat_id, text, pinned=False, parse_mode=None, reply_markup=None, reply_to_message_id=None,
            disable_notification=False, fail_silently=False, api_kwargs=None
    ):
        """
        Отправить сообщение
        """

        return self.send(send_type='message',
                         chat_id=chat_id,
                         text=text,
                         pinned=pinned,
                         parse_mode=parse_mode,
                         reply_markup=reply_markup,
                         reply_to_message_id=reply_to_message_id,
                         disable_notification=disable_notification,
                         fail_silently=fail_silently,
                         api_kwargs=api_kwargs)

    def send_photo(
            self, chat_id, photo, filename=None, caption='', pinned=False, parse_mode=None, reply_markup=None,
            reply_to_message_id=None, disable_notification=False
    ):
        """
        Отправить фото

        photo - либо содержимое файла в bytes, либо url строка
        """
        if len(caption) > self.MAX_MESSAGE_LENGTH:
            # https://ts.it-solution.ru/#/ticket/59906/
            caption = '{}...'.format(caption[:self.MAX_MESSAGE_LENGTH - 3])

        try:
            res = self.client.send_photo(
                chat_id,
                BytesIO(photo) if type(photo) == bytes else photo,
                filename=filename,
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                reply_to_message_id=reply_to_message_id,
                disable_notification=disable_notification
            )
            if pinned:
                self.client.pin_chat_message(chat_id, res.message_id)

            effective_attachment = {}
            if res.effective_attachment:
                effective_attachment = {
                    'photo': [
                        {
                            'file_id': photo_size['file_id'] if hasattr(photo_size, 'file_id') else '',
                            'file_size': photo_size['file_size'] if hasattr(photo_size, 'file_size') else '',
                            'file_unique_id': photo_size['file_unique_id'] if hasattr(photo_size,
                                                                                      'file_unique_id') else '',
                            'height': photo_size['height'] if hasattr(photo_size, 'height') else '',
                            'width': photo_size['width'] if hasattr(photo_size, 'width') else ''
                        } for photo_size in res.effective_attachment
                    ]
                }
            return self.MESSAGE_CLASS(
                telegram_id=res.message_id,
                chat=self.CHAT_CLASS.objects.get(telegram_id=chat_id),
                caption=res.caption,
                effective_attachment=effective_attachment
            )
        except BadRequest as e:
            if e.message.startswith("Can't parse entities") and parse_mode != 'Markdown':
                # Рекурсивно вызовем
                return self.send_photo(chat_id=chat_id,
                                       photo=photo,
                                       filename=filename,
                                       caption=caption,
                                       pinned=pinned,
                                       parse_mode='Markdown',
                                       reply_markup=reply_markup,
                                       reply_to_message_id=reply_to_message_id,
                                       disable_notification=disable_notification)
            else:
                ilogger.error(
                    'telegram_bad_request',
                    'failed to send photo (chat_id=%s, bot_id=%s): %s' % (chat_id, self.id, e.message)
                )
        except ChatMigrated as exc:
            ilogger.warning('telegram_bot_ChatMigrated', 'chat migrated {} => {}'.format(chat_id, exc.new_chat_id))
            if self.RAISE_CHAT_MIGRATED_ERROR:
                raise
        except Exception as exc:
            ilogger.error(
                'telegram_bot_error=> failed to send photo (chat_id=%s, bot_id=%s): %s' % (chat_id, self.id, exc)
            )

        return False

    def send_document(
            self, chat_id, document, filename=None, caption='', pinned=False, parse_mode=None, reply_markup=None,
            reply_to_message_id=None, disable_notification=False, thumb=None, disable_content_type_detection=None
    ):
        """
        Отправить документ (файл)

        document - либо содержимое файла в bytes, либо url строка
        """
        if len(caption) > self.MAX_MESSAGE_LENGTH:
            # https://ts.it-solution.ru/#/ticket/59906/
            caption = '{}...'.format(caption[:self.MAX_MESSAGE_LENGTH - 3])

        try:
            res = self.client.send_document(
                chat_id,
                BytesIO(document) if type(document) == bytes else document,
                filename=filename,
                caption=caption,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                reply_to_message_id=reply_to_message_id,
                disable_notification=disable_notification,
                thumb=thumb,
                disable_content_type_detection=disable_content_type_detection
            )
            if pinned:
                self.client.pin_chat_message(chat_id, res.message_id)

            effective_attachment = {}
            if res.effective_attachment:
                effective_attachment_thumb = {}
                if hasattr(res.effective_attachment, 'thumb') and res.effective_attachment['thumb']:
                    effective_attachment_thumb = {
                        'file_id': res.effective_attachment['thumb']['file_id'] if hasattr(
                            res.effective_attachment['thumb'], 'file_id') else '',
                        'file_size': res.effective_attachment['thumb']['file_size'] if hasattr(
                            res.effective_attachment['thumb'], 'file_size') else '',
                        'file_unique_id': res.effective_attachment['thumb']['file_unique_id'] if hasattr(
                            res.effective_attachment['thumb'], 'file_unique_id') else '',
                        'height': res.effective_attachment['thumb']['height'] if hasattr(
                            res.effective_attachment['thumb'], 'height') else '',
                        'width': res.effective_attachment['thumb']['width'] if hasattr(
                            res.effective_attachment['thumb'], 'width') else ''
                    }
                effective_attachment = {
                    'document': {
                        'file_id': res.effective_attachment['file_id'] if hasattr(res.effective_attachment,
                                                                                  'file_id') else '',
                        'file_name': res.effective_attachment['file_name'] if hasattr(res.effective_attachment,
                                                                                      'file_name') else '',
                        'file_size': res.effective_attachment['file_size'] if hasattr(res.effective_attachment,
                                                                                      'file_size') else '',
                        'file_unique_id': res.effective_attachment['file_unique_id'] if hasattr(
                            res.effective_attachment, 'file_unique_id') else '',
                        'mime_type': res.effective_attachment['mime_type'] if hasattr(res.effective_attachment,
                                                                                      'mime_type') else '',
                        'thumb': effective_attachment_thumb
                    }
                }
            return self.MESSAGE_CLASS(
                telegram_id=res.message_id,
                chat=self.CHAT_CLASS.objects.get(telegram_id=chat_id),
                caption=res.caption,
                effective_attachment=effective_attachment
            )
        except BadRequest as e:
            if e.message.startswith("Can't parse entities") and parse_mode != 'Markdown':
                # Рекурсивно вызовем
                return self.send_document(chat_id=chat_id,
                                          document=document,
                                          filename=filename,
                                          caption=caption,
                                          pinned=pinned,
                                          parse_mode='Markdown',
                                          reply_markup=reply_markup,
                                          reply_to_message_id=reply_to_message_id,
                                          disable_notification=disable_notification,
                                          thumb=thumb,
                                          disable_content_type_detection=disable_content_type_detection)
            else:
                ilogger.error(
                    'telegram_bad_request',
                    'failed to send document (chat_id=%s, bot_id=%s): %s' % (chat_id, self.id, e.message)
                )
        except ChatMigrated as exc:
            ilogger.warning('telegram_bot_ChatMigrated', 'chat migrated {} => {}'.format(chat_id, exc.new_chat_id))
            if self.RAISE_CHAT_MIGRATED_ERROR:
                raise
        except Exception as exc:
            ilogger.error(
                'telegram_bot_error=> failed to send document (chat_id=%s, bot_id=%s): %s' % (chat_id, self.id, exc)
            )

        return False

    def send_voice(
            self, chat_id, voice, filename=None, caption='', duration=None, pinned=False, parse_mode=None,
            reply_markup=None, reply_to_message_id=None, disable_notification=False, thumb=None,
    ):
        """
        Отправить голосовое сообщение

        """
        if len(caption) > self.MAX_MESSAGE_LENGTH:
            # https://ts.it-solution.ru/#/ticket/59906/
            caption = '{}...'.format(caption[:self.MAX_MESSAGE_LENGTH - 3])

        try:
            res = self.client.send_voice(
                chat_id,
                voice,
                filename=filename,
                caption=caption,
                duration=duration,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                reply_to_message_id=reply_to_message_id,
                disable_notification=disable_notification,
            )
            if pinned:
                self.client.pin_chat_message(chat_id, res.message_id)
            #  все что ниже брал из send_document()
            effective_attachment = {}
            if res.effective_attachment:
                effective_attachment_thumb = {}
                if hasattr(res.effective_attachment, 'thumb') and res.effective_attachment['thumb']:
                    effective_attachment_thumb = {
                        'file_id': res.effective_attachment['thumb']['file_id'] if hasattr(
                            res.effective_attachment['thumb'], 'file_id') else '',
                        'file_size': res.effective_attachment['thumb']['file_size'] if hasattr(
                            res.effective_attachment['thumb'], 'file_size') else '',
                        'file_unique_id': res.effective_attachment['thumb']['file_unique_id'] if hasattr(
                            res.effective_attachment['thumb'], 'file_unique_id') else '',
                        'height': res.effective_attachment['thumb']['height'] if hasattr(
                            res.effective_attachment['thumb'], 'height') else '',
                        'width': res.effective_attachment['thumb']['width'] if hasattr(
                            res.effective_attachment['thumb'], 'width') else ''
                    }
                effective_attachment = {
                    'document': {
                        'file_id': res.effective_attachment['file_id'] if hasattr(res.effective_attachment,
                                                                                  'file_id') else '',
                        'file_name': res.effective_attachment['file_name'] if hasattr(res.effective_attachment,
                                                                                      'file_name') else '',
                        'file_size': res.effective_attachment['file_size'] if hasattr(res.effective_attachment,
                                                                                      'file_size') else '',
                        'file_unique_id': res.effective_attachment['file_unique_id'] if hasattr(
                            res.effective_attachment, 'file_unique_id') else '',
                        'mime_type': res.effective_attachment['mime_type'] if hasattr(res.effective_attachment,
                                                                                      'mime_type') else '',
                        'thumb': effective_attachment_thumb
                    }
                }
            return self.MESSAGE_CLASS(
                telegram_id=res.message_id,
                chat=self.CHAT_CLASS.objects.get(telegram_id=chat_id),
                caption=res.caption,
                effective_attachment=effective_attachment
            )
        except BadRequest as e:
            if e.message.startswith("Can't parse entities") and parse_mode != 'Markdown':
                # Рекурсивно вызовем
                return self.send_voice(chat_id=chat_id,
                                       voice=voice,
                                       filename=filename,
                                       caption=caption,
                                       duration=duration,
                                       pinned=pinned,
                                       parse_mode='Markdown',
                                       reply_markup=reply_markup,
                                       reply_to_message_id=reply_to_message_id,
                                       disable_notification=disable_notification, )
            else:
                ilogger.error(
                    'telegram_bad_request',
                    'failed to send voice (chat_id=%s, bot_id=%s): %s' % (chat_id, self.id, e.message)
                )
        except ChatMigrated as exc:
            ilogger.warning('telegram_bot_ChatMigrated', 'chat migrated {} => {}'.format(chat_id, exc.new_chat_id))
            if self.RAISE_CHAT_MIGRATED_ERROR:
                raise
        except Exception as exc:
            ilogger.error(
                'telegram_bot_error=> failed to send voice (chat_id=%s, bot_id=%s): %s' % (chat_id, self.id, exc)
            )

        return False

    def after_updates_handle(self, updates: List[HandledUpdate]):
        """
        Вызывается послее обработки обновлений
        """

        pass

    def edit_message(self, chat_id, message_id, text=None, parse_mode=None, reply_markup=None, delete_markup=False):
        """
        Изменить текст и клавиатуру сообщения

        После изменения текста пропадает клавиатура. Если нужно изменить только текст, но сохранить клавиатуру,
        всё равно нужно передавать reply_markup.
        """

        if text is not None:
            self.__call_edit_method(
                self.client.edit_message_text,
                chat_id=chat_id, message_id=message_id, parse_mode=parse_mode, text=text
            )

        if delete_markup or reply_markup is not None:
            self.__call_edit_method(
                self.client.edit_message_reply_markup,
                chat_id=chat_id, message_id=message_id, reply_markup=reply_markup
            )

    def __call_edit_method(self, method, *args, **kwargs):
        """
        Безопасный вызов метода изменения текста или клавиатуры сообщения
        """

        try:
            method(*args, **kwargs)

        except BadRequest as exc:
            # Телеграм ругается, если пытаeмся передать текст или клавиатуру без изменений
            if self.NO_CHANGES_ERROR_MESSAGE not in exc.message.lower():
                raise
