# pydub используем для переделывания mp3 в wav
from pydub import AudioSegment

# с помощью os записываем пути к файлам
from settings import BASE_DIR
import os

# pathlib используем для прописывания путей к файлам
import pathlib
from pathlib import Path

"""С помощью библиотеки pydub делаем из mp3 файла wav,
   эта функция понадобиться нам ниже, т.к. тиньков не умеет в распознавание mp3 не в реальном времени
"""
file_mp3_path = str(os.path.join(BASE_DIR, 'audio_recognition', 'samples', 'file_for_test.mp3'))
file_wav_path = file_mp3_path[:-3] + 'wav'


def wav_maker():
    """С помощью библиотеки pydub делаем из mp3 файла wav,
       эта функция понадобиться нам ниже, т.к. тиньков не умеет в распознавание mp3 не в реальном времени
    """
    AudioSegment.from_mp3(file_mp3_path).export(file_wav_path, format="wav")
