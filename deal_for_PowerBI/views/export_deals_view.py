from datetime import date, timedelta

from django.http import JsonResponse, HttpResponseForbidden

from integration_utils.bitrix24.models import BitrixUser
from integration_utils.its_utils.app_get_params import get_params_from_sources


@get_params_from_sources
def export_deals(request):
    """
    Функция отвечает за сбор данных из битрикса, обработку в нужный вид и
    отправку в PowerBI.
    """
    if request.its_params.get('s') != 'KJBHILiswbeg8yuesbg':
        return HttpResponseForbidden()
    but = BitrixUser.objects.filter(is_admin=True,
                                    user_is_active=True).first().bitrix_user_token
    deals = but.call_list_method('crm.deal.list', {
        'select': ['ASSIGNED_BY_ID', 'COMPANY_ID', 'CONTACT_IDS',
                   'DATE_CREATE', 'TITLE']})
    companies = but.call_list_method('crm.company.list', {
        'select': ['ADDRESS', 'ADDRESS_CITY', 'ID', 'LEAD_ID', 'TITLE']})
    contacts = but.call_list_method('crm.contact.list', {
        'select': ['ID', 'LEAD_ID', 'NAME', 'LAST_NAME', 'COMPANY_IDS']})
    result = {
        'deals': deals,
        'companies': companies,
        'contacts': contacts
    }
    return JsonResponse(result, safe=False)

