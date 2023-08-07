import requests
import time
from .secondary_utils import *
from dateutil.parser import parse


from integration_utils.vendors.telegram import Bot

CALLS_TYPES = {
    '1': 'Исходящий звонок',
    '2': 'Входящий звонок',
    '3': 'Входящий с перенаправлением (на мобильный или стационарный телефон)',
    '4': 'Обратный звонок',
    None: 'Нет данных'
}


def keep_call_info_synced(bot_token, calls_chat_id):
    bot = Bot(token=bot_token)
    while True:
        but = get_auth()
        try:
            last_call_id = but.call_api_method('app.option.get', {})['result']['last_call_id']
        except KeyError:
            # если вдруг в базе нет последнего id, берем последний звонок
            last_call_id = but.call_list_method('voximplant.statistic.get', {'SORT': 'ID', 'ORDER': 'DESC'}, limit=1)[0]['ID']
        last_call_id = send_calls(but, bot, calls_chat_id, last_call_id, mode="strictly-larger")
        if last_call_id is not None:
            but.call_api_method('app.option.set', {'options': {'last_call_id': last_call_id}})
        flag = but.call_api_method('app.option.get', {})['result']['call_sync_flag']
        if flag == "false":
            print("quitting sync loop")
            break
        time.sleep(10)


def export_calls_to_telegram(bot_token, calls_chat_id):
    but = get_auth()
    bot = Bot(token=bot_token)
    call_id = '0'

    last_call_id = send_calls(but, bot, calls_chat_id, call_id, mode="equal-or-larger")
    if last_call_id is not None:
        but.call_api_method('app.option.set', {'options': {'last_call_id': last_call_id}})
        return True
    else:
        return False


def send_calls(but, bot, calls_chat_id, call_id, mode):
    # отсылаем все подряд, начиная со звонка, имеющего call_id
    # проходимся по всем звонкам в заданном параметром mode диапазоне и добавляем их в запрос по id
    calls_with_files, len_calls = get_calls_with_files(but, call_id, mode)
    if len_calls != 0:
        methods = []
        for c in calls_with_files.values():
            methods.append(('disk.file.get', {'id': c['RECORD_FILE_ID']}))
        call_files = but.batch_api_call(methods)

        msges = 0
        users = get_users(but)
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
    else:
        return None


