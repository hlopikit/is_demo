import os
import urllib.request

import requests
from django.conf import settings
from django.shortcuts import render

from demo_data_in_bitrix.views.utils import excel_to_dict, get_sheet_names, OBJECT_CRM, import_data_from_xls
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.core.files.storage import FileSystemStorage

from integration_utils.its_utils.app_get_params import get_params_from_sources
from integration_utils.its_utils.app_get_params.decorators import expect_param


@main_auth(on_cookies=True)
# достает из GET, POST, json тела парметры
@get_params_from_sources
@expect_param('link', coerce=str)
def load_from_googledocs(request, link):
    but = request.bitrix_user_token

    # Ожидаем что люди нам будут скармливать ссылки типа https://docs.google.com/spreadsheets/d/1ZuKXEK0hwJyxFwGxoi77G0PaOh4Qg4SDZBNkHDws2iU/edit#gid=1891471437
    # а нам нужно вместо edit, делать export
    # сделаем преобразование разбиением строки. Может сбойнуть если id документа будет начинаться с edit
    export_link = link.split("/edit")[0] + "/export"
    # вариант 2
    export_link = "/".join(link.split("/")[0:-1]) + "/export"
    res = requests.get(export_link)
    filename = os.path.join(settings.BASE_DIR, 'temp.xlsx')
    with open(filename, "wb") as f:
        f.write(res.content)
    import_data_from_xls(filename, but)

    return render(request, 'demodata.html', locals())
