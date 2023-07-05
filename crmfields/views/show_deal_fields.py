from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def show_deal_fields(request):
    but = request.bitrix_user_token
    res = but.call_api_method("crm.deal.fields")['result']
    total_value = len(res)
    return render(request, 'showdealfields.html', locals())

