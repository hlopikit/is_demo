from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def select_user(request):
    but = request.bitrix_user_token
    table = False

    if request.method == 'POST':
        table = True
        user_id = request.POST['user']
        res = but.call_api_method("user.get", {'ID': user_id})['result'][0]

    return render(request, 'selectuser.html', locals())