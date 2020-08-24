import json

from django.shortcuts import render
from django.conf import settings

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from integration_utils.ones.functions.guids_converts import guid_to_non_separated


@main_auth(on_start=True, set_cookie=True)
#@ones_user_auth()
def company_placement(request):
    unf_base_url = settings.ONES_FRESH_UNF_WITH_B24_SETTINGS.unf_base_url
    bitrix_user_token = request.bitrix_user_token
    #app_settings = settings.APP_SETTINGS
    #username = request.ones_username
    #password = request.ones_password
    company_id = json.loads(request.POST.get('PLACEMENT_OPTIONS')).get('ID')
    company = bitrix_user_token.call_api_method('crm.company.get', {"ID": company_id})['result']
    if company.get('ORIGIN_ID'):
        guid = guid_to_non_separated(company.get('ORIGIN_ID'))
    return render(request, 'company_placement.html', locals())