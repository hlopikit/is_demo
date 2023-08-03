from django.utils.module_loading import import_string


def handle_bot_updates(class_path=None):
    if not class_path:
            raise Exception('Не указан class_path')

    BotClass = import_string(class_path)

    from telegram.vendor.ptb_urllib3 import urllib3
    urllib3.disable_warnings()

    replies_count = command_count = fails_count = 0
    active_bot = BotClass.objects.filter(is_active=True).last()
    if active_bot:
        replies_count, command_count, fails_count = active_bot.handle_updates()

    return 'updates handled: {}, commands handled: {}, commands failed: {}'.format(
        replies_count, command_count, fails_count
    )
