import requests
from dateutil.parser import parse

from integration_utils.bitrix24.exceptions import BitrixApiError
from integration_utils.bitrix24.models import BitrixUserToken
from telegram import Bot
import asyncio
from django.conf import settings

CALLS_TYPES = {
    '1': 'Исходящий звонок',
    '2': 'Входящий звонок',
    '3': 'Входящий с перенаправлением (на мобильный или стационарный телефон)',
    '4': 'Обратный звонок',
    None: 'Нет данных'
}


def keep_call_info_synced(bot_token, calls_chat_id):
    but = get_auth()
    bot = Bot(token=bot_token)
    try:
        last_call_id = but.call_api_method('app.option.get', {})['result']['last_call_id']
    except KeyError:
        # если вдруг в базе нет последнего id, берем последний звонок
        last_call_id = str(int(but.call_list_method('voximplant.statistic.get', {'SORT': 'ID', 'ORDER': 'DESC'}, limit=1)[0]['ID']))
    last_call_id = send_calls(but, bot, calls_chat_id, last_call_id, mode="strictly-larger")
    but.call_api_method('app.option.set', {'options': {'last_call_id': last_call_id}})


def export_calls_to_telegram(bot_token, calls_chat_id):
    but = get_auth()
    bot = Bot(token=bot_token)
    call_id = '0'

    last_call_id = send_calls(but, bot, calls_chat_id, call_id, mode="equal-or-larger")
    but.call_api_method('app.option.set', {'options': {'last_call_id': last_call_id}})


def get_auth():
    return BitrixUserToken.objects.filter(user__is_admin=True, is_active=True).first()


def get_users(but):
    users = but.call_list_method('user.get', {'ADMIN_MODE': True})
    users = {u['ID']: u for u in users}
    return users


def get_calls_with_files(but, last_id, mode):
    if mode == "strictly-larger":
        filter_dict = {'FILTER': {'>ID': last_id}}
    elif mode == "equal-or-larger":
        filter_dict = {'FILTER': {'>=ID': last_id}}
    else:
        raise ValueError
    calls = but.call_list_method('voximplant.statistic.get', filter_dict)
    calls_with_files = {c['RECORD_FILE_ID']: c for c in calls if c.get('RECORD_FILE_ID')}
    return calls_with_files, len(calls)


def add_entity_url(but, call):
    if call.get('CRM_ENTITY_TYPE'):
        url = f"https://{settings.APP_SETTINGS.app_domain}/crm/{call['CRM_ENTITY_TYPE'].lower()}/details/{call['CRM_ENTITY_ID']}/"
        try:
            entity = but.call_list_method(f"crm.{call['CRM_ENTITY_TYPE'].lower()}.get", {'ID': call['CRM_ENTITY_ID'].lower()})
            name = f"{entity['LAST_NAME']} {entity['NAME']}".strip() if (entity.get('NAME') or entity.get('LAST_NAME')) else entity['TITLE']
        except BitrixApiError as e:
            if 'Not found' in str(e):
                name = f"{call['CRM_ENTITY_TYPE']} с id = {call['CRM_ENTITY_ID']}"
            else:
                raise
        return f"[{name}]({url})\n"
    return ''


def send_calls(but, bot, calls_chat_id, call_id, mode):
    # отсылаем все подряд, начиная со звонка, имеющего call_id
    # проходимся по всем звонкам в заданном параметром mode диапазоне и добавляем их в запрос по id
    calls_with_files, len_calls = get_calls_with_files(but, call_id, mode)
    methods = []
    for c in calls_with_files.values():
        methods.append(('disk.file.get', {'id': c['RECORD_FILE_ID']}))
    call_files = but.batch_api_call(methods)

    msges = 0
    users = get_users(but)
    if len(call_files.values()) != 0:
        loop = asyncio.new_event_loop()
    for f in call_files.successes.values():
        call = calls_with_files[int(f['result']['ID'])]
        start = parse(call['CALL_START_DATE'])
        msg = f"{CALLS_TYPES[call['CALL_TYPE']]}\n" \
              f"{start.strftime('%d.%m.%Y %H:%M:%S')}\n" \
              f"Номер {call['PHONE_NUMBER']} \n" \
              f"Менеджер: {get_user_name(users, call['PORTAL_USER_ID'])}\n" \
              f"{call['CRM_ENTITY_TYPE'].capitalize() if call['CRM_ENTITY_TYPE'] else 'Нет данных'}: "
        msg += add_entity_url(but, call)
        file_content = requests.get(f['result']['DOWNLOAD_URL'])
        file_content = file_content.content
        res = bot.send_audio(
            chat_id=calls_chat_id,
            audio=file_content,
            filename=f['result']['NAME'],
            caption=msg,
        )
        call_id = str(int(call_id) + 2)
        msges += 1 if res else 0

    return call_id


def get_user_name(users, user_id):
    user = users[user_id]
    name = f"{user['LAST_NAME']} {user['NAME']}".strip()
    return f"[{name}](https://{settings.APP_SETTINGS.app_domain}/company/personal/user/{user_id}/)"