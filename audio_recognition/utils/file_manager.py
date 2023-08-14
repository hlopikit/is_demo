import os
from settings import BASE_DIR


def save_file(audio_file):
    # сохраняет файл
    file_path = os.path.join(BASE_DIR, 'audio_recognition', 'samples', audio_file.name)
    with open(file_path, 'wb') as f:
        for chunk in audio_file.chunks():
            f.write(chunk)
    return file_path


def remove_file(file_path):
    # удаляет файл
    if os.path.isfile(file_path):
        os.remove(file_path)
