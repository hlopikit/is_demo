# Нужные импорты
import openai

from django.conf import settings
from settings import BASE_DIR
import os

# Ключ с openai API
openai.api_key = settings.OPEN_AI_API_KEY


# Сама функция, где берем файл и прогоняем его через openai
def open_ai_get_text():
    audio_file = open(str(os.path.join(BASE_DIR, 'audio_recognition', 'samples', 'file_for_test.mp3')), "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.text
