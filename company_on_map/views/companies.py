from django.http import JsonResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def companies(request):
    """Возвращает JSON со списком компаний с известными адресами"""
    but = request.bitrix_user_token
    all_companies = but.call_list_method("crm.company.list", {
        "select": ["ID", "TITLE"]
    })
    all_companies = {c["ID"]: c for c in all_companies}

    all_addresses = but.call_list_method("crm.address.list", {
        "order": {"TYPE_ID": "ASC"},
        "select": ["ADDRESS_1", "PROVINCE", "COUNTRY", "ANCHOR_ID"],
        "filter": {
            "ANCHOR_TYPE_ID": "4"
        }
    })

    comps_w_addr = {}
    for a in all_addresses:
        comp = comps_w_addr.setdefault(a["ANCHOR_ID"], {})
        comp.setdefault("addr", []).append(a)
        comp["title"] = all_companies[a["ANCHOR_ID"]]["TITLE"]

    return JsonResponse(all_companies)
