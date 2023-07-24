import pytz

from datetime import datetime, timedelta


def parse_datetime(date_str):

    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return dt.astimezone(pytz.timezone('Europe/Moscow'))


def filter_yesterday_day(data_list):

    now = pytz.timezone('Europe/Moscow').localize(datetime.now())
    yesterday = now - timedelta(days=1)
    start_of_yesterday = yesterday.replace(hour=0, minute=0, second=0,
                                           microsecond=0)
    end_of_yesterday = yesterday.replace(hour=23, minute=59, second=59,
                                         microsecond=999999)

    filtered_data_list = [d for d in data_list if
                          start_of_yesterday <= parse_datetime(
                              d['CALL_START_DATE']) <= end_of_yesterday]

    return filtered_data_list


def parse_date(date_str):

    parsed_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    formatted_date = parsed_date.strftime("%d %b %Y, %H:%M:%S")

    return formatted_date


def call_type(call):

    res = {
        '1': 'Исходящий',
        '2': 'Входящий',
        '3': 'Входящий с перенаправлением',
        '4': 'Обратный звонок',
    }

    return res[call]
