from django.shortcuts import render

from audio_recognition.utils.openai_recon import open_ai_get_text
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def show_info_open_ai(request):
    if request.method == 'POST':
        recon_txt = open_ai_get_text()
        return render(request, 'show_info.html',
                      context={'recognized_text_open_ai': recon_txt})
    return render(request, 'show_info.html')
