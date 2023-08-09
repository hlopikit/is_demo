from django.shortcuts import render
from audio_recognition.utils.openai_recon import open_ai_get_text
from audio_recognition.utils.file_manager import save_file, remove_file
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def upload_audio_open_ai(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        # сохраняем файл и получем путь
        file_path = save_file(audio_file)
        # рапознование текста
        recon_txt = open_ai_get_text(audio_file.name)
        # удалание файла
        remove_file(file_path)
        return render(request, 'show_info.html',
                      context={'upload_recognized_text_open_ai': recon_txt})
    return render(request, "show_info.html")
