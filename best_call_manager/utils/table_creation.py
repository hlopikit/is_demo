from best_call_manager.utils.call_type import get_call_type
from best_call_manager.utils.datetime_utils import parse_date
from django.conf import settings


def add_row(table, counter, row):
    """Позволяет добавить в таблицу строчку с нужными данными"""

    table.add_row([f'{counter}',
                   row.loc['CALL_ID'],
                   row.loc['PHONE_NUMBER'],
                   parse_date(row.loc['START_DATETIME']),
                   f"{row.loc['DURATION']} секунд",
                   get_call_type(row.loc['CALL_TYPE'])])


def add_row_to_df(df, call):
    """Позволяет добавить запись в DateFrame"""

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


def get_html_row(call, calls, counter):
    """Создает строчку с данными о лучшем звонке менеджера"""

    row = f"""<tr>
                    <td>    {counter}   </td>
                    <td>    {calls[call['ID']]}  </td>
                    <td>    {call['ID']}    </td>
                    <td>    {call['PHONE_NUMBER']}  </td>
                    <td><a href='https://{settings.APP_SETTINGS.portal_domain}/disk/downloadFile/{call['RECORD_FILE_ID']}/'>Скачать</a></td>
                    <td>    {call['CALL_DURATION']} секунд  </td>
                    <td>    {parse_date(call['CALL_START_DATE'])}  </td>
                    <td>    {get_call_type(call['CALL_TYPE'])}  </td>
                </tr>\n"""

    return row


def get_html_table(rows):
    """Создает таблицу с данными о лучших звонках менеджеров"""

    html_table = f"""<table>
                    <tr>
                        <th>№</th>
                        <th>Менеджер</th>
                        <th>ID звонка</th>
                        <th>Номер</th>
                        <th>Запись звонка</th>
                        <th>Длительность</th>
                        <th>Дата</th>
                        <th>Тип</th>
                    </tr>
                    {rows}
                </table>"""

    return html_table
