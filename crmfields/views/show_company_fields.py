from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def show_company_fields(request):

    but = request.bitrix_user_token
    res = but.call_api_method("crm.company.fields")['result']
    quantity_fields = len(res)

    return render(request, 'showcompanyfields.html', locals())
