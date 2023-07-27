from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..forms import CallInfoForm



@main_auth(on_cookies=True)
def reg_call(request):
    but = request.bitrix_user_token
    if request.method == 'POST':
        form = CallInfoForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            model.telephony_externalcall_register(but)
            model.telephony_externalcall_finish(but)
            model.wav_maker_n_messages(but)
    form = CallInfoForm()
    return render(request, 'registercall.html', locals())
