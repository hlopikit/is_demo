from django.conf import settings

from integration_utils.bitrix24.models import BitrixUserToken


def register_placement():
    but = BitrixUserToken.objects.filter(is_active=True, user__is_admin=True).first()
    return but.call_api_method('placement.bind',
                        {'title': "В 1С",
                         'handler': 'https://{}/ones/company_placement/'.format(settings.APP_SETTINGS.app_domain),
                         'placement': 'CRM_COMPANY_DETAIL_TAB'})
