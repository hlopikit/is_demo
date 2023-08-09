# pydub используем для переделывания mp3 в wav
from pydub import AudioSegment

# с помощью os записываем пути к файлам
from settings import BASE_DIR
import os


"""С помощью библиотеки pydub делаем из mp3 файла wav,
   эта функция понадобиться нам ниже, т.к. тиньков не умеет в распознавание mp3 не в реальном времени
"""


def wav_maker(filename):
    """С помощью библиотеки pydub делаем из mp3 файла wav,
       эта функция понадобиться нам ниже, т.к. тиньков не умеет в распознавание mp3 не в реальном времени
    """

    file_mp3_path = str(os.path.join(BASE_DIR, 'audio_recognition', 'samples',
                                     filename))
    file_wav_path = get_wav_path(file_mp3_path)

    AudioSegment.from_mp3(file_mp3_path).export(file_wav_path, format='wav')

    return file_wav_path


def get_wav_path(file_path):
    return file_path[:-3] + 'wav'
