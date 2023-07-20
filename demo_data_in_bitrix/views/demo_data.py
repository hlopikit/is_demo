import os
import urllib.request

from django.shortcuts import render

from demo_data_in_bitrix.views.utils import excel_to_dict, get_sheet_names
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def excel(request):

    if request.method == 'POST':
        data = []
        sheet_names = get_sheet_names('table.xlsx')
        print(sheet_names)
        try:
            response = urllib.request.urlretrieve(request.POST['link'], "table.xlsx")
            data = excel_to_dict('table.xlsx', "Компании")

            but = request.bitrix_user_token
            but.call_api_method("crm.item.batchImport", {"entityTypeId": 4,
                                                         "data": data})
            result = "Компании успешно добавлены!"
        except Exception as Ex:
            result = "Неверная ссылка"

    return render(request, 'demodata.html', locals())
