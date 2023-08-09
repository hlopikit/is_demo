from django.shortcuts import render
import os
from settings import BASE_DIR
from audio_recognition.utils.openai_recon import open_ai_get_text
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def upload_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        file_path = os.path.join(BASE_DIR, 'audio_recognition', 'samples',
                                 audio_file.name)
        with open(file_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)
        recon_txt = open_ai_get_text(audio_file.name)
        os.remove(file_path)
        return render(request, 'show_info.html',
                      context={'upload_recognized_text_open_ai': recon_txt})
    return render(request, "show_info.html")
