from django.shortcuts import render
from audio_recognition.utils.get_text import get_text
from audio_recognition.utils.mp3_to_wav import get_wav_path
from audio_recognition.utils.file_manager import save_file, remove_file
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def upload_audio_tinkoff(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        # сохраняем файл и получем путь
        file_path = save_file(audio_file)
        # рапознование текста
        recon_txt = get_text(audio_file.name)
        # удалание файлов
        remove_file(file_path)
        remove_file(get_wav_path(file_path))
        return render(request, 'show_info.html',
                      context={'upload_recognized_text_tinkoff': recon_txt})
    return render(request, "show_info.html")
