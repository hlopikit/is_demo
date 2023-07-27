from datetime import datetime


def parse_date(date_str):
    """Позволяет распарсить дату в удобочитаемом формате."""

    parsed_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    formatted_date = parsed_date.strftime("%d %b %Y, %H:%M:%S")

    return formatted_date
