import re

from its_utils.app_regexp.constants import REGEXP_DOMAIN

REGEX_PHONE = '\+?\d ?\(?\d\d\d\)? ?\d\d\d ?-?\d\d ?-?\d\d'
REGEX_EMAIL = "([A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+)"

ALLOWED_TAGS = ['b', 'strong', 'i', 'em', 'code', 's', 'strike', 'del', 'u', 'pre', 'a', 'tg-spoiler']


def get_command_from_message(message, bot_username, bot_to_check=None):
    """
    Получить первую команду из сообщенияю. Весь текст после команды считается параметром.
    Текст до команды игнорируется.

    https://core.telegram.org/bots/api#messageentity
    """

    res_command = res_params = None
    for entity in message['entities']:
        if entity['type'] == entity.BOT_COMMAND:
            start = entity['offset']
            end = entity['offset'] + entity['length']
            command = message['text'][start:end]
            params = message['text'][end:].strip()

            # В группе может быть несколько ботов, поэтому команды имею вид /команда@имя_бота
            match = re.match('(/\w+)@(\w+)', command)
            if match:
                command, mention = match.groups()
                if mention != bot_username:
                    # команда пришла не нашему боту
                    continue

            if bot_to_check is not None:
                command_exists = bot_to_check.get_command(command)
                if not command_exists:
                    continue

            res_command, res_params = command, params

            break

    return res_command, res_params


def is_mentioned(message, username):
    """
    Найти упоминание пользователя в сообщении

    https://core.telegram.org/bots/api#messageentity
    """

    user_mention = '@{}'.format(username)
    for entity in message['entities']:
        if entity['type'] == entity.MENTION:
            start = entity['offset']
            end = entity['offset'] + entity['length']
            if message['text'][start:end] == user_mention:
                return True

    return False


def is_reply(message, username):
    return message.reply_to_message and message.reply_to_message.from_user.username == username


BOT_ID_MASK = 10 ** 12


def find_contacts_in_text(text):
    phones = re.findall(REGEX_PHONE, text)
    emails = re.findall(REGEX_EMAIL, text)
    domains = re.findall(REGEXP_DOMAIN, text)

    return list(set(phones + emails + domains) - set([x.split('@')[1] for x in emails]))


def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def escape_disallowed_tags(text):
    import bleach
    return bleach.clean(text, tags=ALLOWED_TAGS)
