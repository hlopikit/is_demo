from best_call_manager.utils.call_type import get_call_type
from best_call_manager.utils.datetime_utils import parse_date


def add_row(table, counter, row):
    """Позволяет добавить в таблицу строчку с нужными данными."""

    table.add_row([f'{counter}',
                   row.loc['CALL_ID'],
                   row.loc['PHONE_NUMBER'],
                   parse_date(row.loc['START_DATETIME']),
                   f"{row.loc['DURATION']} секунд",
                   get_call_type(row.loc['CALL_TYPE'])])


def add_row_in_df(df, call):
    row = [
        call["ID"],
        call["PORTAL_USER_ID"],
        call["PHONE_NUMBER"],
        call["CALL_START_DATE"][:10],
        call["CALL_START_DATE"],
        call["CALL_DURATION"],
        call["CALL_TYPE"]
    ]
    df.loc[len(df.index)] = row
