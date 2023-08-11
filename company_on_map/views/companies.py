from django.http import JsonResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def companies(request):
    """Возвращает JSON со списком компаний с известными адресами"""
    but = request.bitrix_user_token
    all_companies = but.call_list_method("crm.company.list", {
        "select": ["ID", "TITLE"]
    })
    all_companies = {c["ID"]: c for c in all_companies.items()}

    return JsonResponse(all_companies)
