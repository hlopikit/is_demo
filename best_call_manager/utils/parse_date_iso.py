from datetime import datetime


def parse_date_iso(date):
    """Позволяет преобразовать дату: 23 Jul 2023 ->> 23.07.2023"""

    date_obj = datetime.strptime(date, "%d %b %Y")
    formatted_date = date_obj.strftime("%d.%m.%Y")

    return formatted_date
