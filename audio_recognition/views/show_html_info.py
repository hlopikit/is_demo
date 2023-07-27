from django.shortcuts import render

from audio_recognition.utils.get_text import get_text
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def show_info(request):
    if request.method == 'POST':
        recon_txt = get_text()
        return render(request, 'show_info.html', context={'recognized_text': recon_txt})
    return render(request, 'show_info.html')
