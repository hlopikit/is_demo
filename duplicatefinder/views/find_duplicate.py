from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from collections import Counter


@main_auth(on_cookies=True)
def find_duplicates(request):
    but = request.bitrix_user_token
    lst = list()
    res = but.call_list_method('crm.product.list')
    for i in res:
        lst.append(i["NAME"])
    res = {name: count for name, count in Counter(lst).items() if count > 1}
    return render(request, 'duplicates.html', context={'res': res})
