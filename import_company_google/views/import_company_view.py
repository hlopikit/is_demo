import os

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
import csv
import urllib.request


@main_auth(on_cookies=True)
def import_company_google(request):
    if request.method == 'POST':
        data = []
        try:
            response = urllib.request.urlretrieve(request.POST['link'], "table.csv")
            with open('table.csv', encoding='UTF-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
            os.remove('table.csv')

            but = request.bitrix_user_token

            methods = []
            for company in data:
                methods.append(("crm.company.add", {"fields": company}))
            but.batch_api_call(methods)

            result = "Компании успешно добавлены!"
        except Exception as Ex:
            result = "Неверная ссылка"
    return render(request, 'import_company_google.html', locals())
