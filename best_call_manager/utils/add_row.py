from best_call_manager.utils.call_type import call_type
from best_call_manager.utils.parse_date import parse_date


def add_row(table, counter, call):
    """Позволяет добавить в таблицу строчку с нужными данными."""

    table.add_row([f'{counter}', call['ID'],
                   call['PHONE_NUMBER'],
                   parse_date(call['CALL_START_DATE']),
                   f"{call['CALL_DURATION']} секунд",
                   call_type(call['CALL_TYPE'])])
