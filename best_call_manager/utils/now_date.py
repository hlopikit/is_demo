from datetime import datetime


def now_date():
    """Позволяет получить сегодняшнюю дату в iso-формате (дата динамическая,
    время всегда 00:00:00, для того, чтобы получать задачи всего дня)"""

    current_datetime = datetime.now()
    current_datetime = current_datetime.replace(hour=0, minute=0, second=0,
                                                microsecond=0)
    formatted_datetime = current_datetime.isoformat()

    return formatted_datetime
