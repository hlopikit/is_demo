import json

from dateutil import parser
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models import BitrixUserToken
from integration_utils.its_utils.app_get_params import get_params_from_sources

from django.conf import settings


@main_auth(on_cookies=True)
def show_company_fields(request):

    but = request.bitrix_user_token
    res = but.call_api_method("crm.company.fields")['result']
    quantity_fields = len(res)

    return render(request, 'showcompanyfields.html', locals())
