from best_call_manager.utils.call_type import call_type
from best_call_manager.utils.parse_date import parse_date
from local_settings import APP_SETTINGS


def row_in_table(call, calls, counter):
    """Создает строчку с данными о лучшем звонке менеджера."""

    field = f"""<tr>
                    <td>    {counter}   </td>
                    <td>    {calls[call['ID']][0]}  </td>
                    <td>    {call['ID']}    </td>
                    <td>    {call['PHONE_NUMBER']}  </td>
                    <td><a href='https://{APP_SETTINGS.portal_domain}/disk/downloadFile/{call['RECORD_FILE_ID']}/'>Скачать</a></td>
                    <td>    {call['CALL_DURATION']} секунд  </td>
                    <td>    {parse_date(call['CALL_START_DATE'])}  </td>
                    <td>    {call_type(call['CALL_TYPE'])}  </td>
                </tr>\n"""

    return field
