from datetime import datetime


def get_now_date():
    """Позволяет получить сегодняшнюю дату в iso-формате (дата динамическая,
    время всегда 00:00:00, для того, чтобы получать задачи всего дня)"""

    current_datetime = datetime.now()
    current_datetime = current_datetime.replace(hour=0, minute=0, second=0,
                                                microsecond=0)
    formatted_datetime = current_datetime.isoformat()

    return formatted_datetime


def parse_date(date_str):
    """Позволяет распарсить дату в удобочитаемом формате"""

    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    formatted_date = date_obj.strftime("%d %b %Y, %H:%M:%S")

    return formatted_date


def parse_date_in_dmy(date_str):
    """Позволяет преобразовать дату: в d/m/y"""

    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    formatted_date = date_obj.strftime("%d/%m/%Y")

    return formatted_date
