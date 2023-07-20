import os
import urllib.request

from django.shortcuts import render

from demo_data_in_bitrix.views.utils import excel_to_dict, get_sheet_names, OBJECT_CRM
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.core.files.storage import FileSystemStorage


@main_auth(on_cookies=True)
def excel(request):
    if request.method == 'POST':
        but = request.bitrix_user_token
        try:
            filename = None
            if request.POST['link'] != '':
                response = urllib.request.urlretrieve(request.POST['link'], "table.xlsx")
                filename = "table.xlsx"
            else:
                file = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save("test.xlsx", file)
                filename = f'media/{filename}'
            sheet_names = get_sheet_names(filename)
            for sheet_name in sheet_names:
                but = request.bitrix_user_token
                data = excel_to_dict(filename, sheet_name)
                but.call_api_method("crm.item.batchImport", {"entityTypeId": str(OBJECT_CRM[sheet_name]),
                                                             "data": data[0]})
                if sheet_name == "Компании":
                    companies = but.call_list_method('crm.company.list', {"SELECT": {"ORIGIN_ID", "ID"}})
                    for company in companies:
                        ORIGIN_ID = int(float(company['ORIGIN_ID']))
                        if ORIGIN_ID in list(data[1].keys()):
                            data[1][ORIGIN_ID] = company['ID']
                index = 1
                for row in data[2]:
                    but.call_api_method("crm.address.add", {"fields": {
                        "TYPE_ID": "1",
                        "ENTITY_TYPE_ID": "4",
                        "ENTITY_ID": data[1][index],
                        "CITY": row["CITY"],
                        "ADDRESS_1": row["ADDRESS_1"],
                    }})
                    index += 1
            result = "Сущности успешно добавлены!"
        except Exception as Ex:
            result = "Неверная ссылка"

    return render(request, 'demodata.html', locals())
