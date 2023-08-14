import requests
import time
from .secondary_utils import *


from integration_utils.vendors.telegram import Bot


def keep_call_info_synced(but, bot_token, calls_chat_id):
    bot = Bot(token=bot_token)
    while True:
        try:
            last_call_id = but.call_api_method('app.option.get')['result']['last_call_id']
        except TypeError:
            # если вдруг в базе нет последнего id, берем последний звонок
            last_call_id = but.call_list_method('voximplant.statistic.get', {'SORT': 'ID', 'ORDER': 'DESC'}, limit=1)[0]['ID']
        first_call_id = str(int(last_call_id) + 2)
        last_call_id = send_calls(but, bot, calls_chat_id, first_call_id)
        if last_call_id is not None:
            but.call_api_method('app.option.set', {'options': {'last_call_id': last_call_id}})
        flag = but.call_api_method('app.option.get')['result']['call_sync_flag']
        if flag == "false":
            print("quitting sync loop")
            break
        time.sleep(10)


def export_calls_to_telegram(but, bot_token, calls_chat_id):
    bot = Bot(token=bot_token)
    first_call_id = '0'

    last_call_id = send_calls(but, bot, calls_chat_id, first_call_id)
    if last_call_id is not None:
        but.call_api_method('app.option.set', {'options': {'last_call_id': last_call_id}})
        return True
    else:
        return False


def send_calls(but, bot, calls_chat_id, first_call_id):
    # отсылаем все подряд, начиная со звонка, имеющего call_id
    # проходимся по всем звонкам в заданном параметром mode диапазоне и добавляем их в запрос по id
    calls_with_files, len_calls = get_calls_with_files(but, first_call_id)
    last_call_id = str(len_calls * 2 + int(first_call_id))
    if not calls_with_files:
        return None

    methods = []
    for file_id in calls_with_files.keys():
        methods.append(('disk.file.get', {'id': file_id}))
    call_files = but.batch_api_call(methods)

    users = get_users(but)
    for call_file in call_files.successes.values():
        call = calls_with_files[int(call_file['result']['ID'])]
        msg = create_message(call, users)
        msg += add_entity_url(but, call)
        file_content = requests.get(call_file['result']['DOWNLOAD_URL'])
        file_content = file_content.content
        bot.send_audio(
            chat_id=calls_chat_id,
            audio=file_content,
            filename=call_file['result']['NAME'],
            caption=msg,
        )

    return last_call_id
