# Импортируем нужные нам файлы из папки тинькова
# Нужные файлы находятся тут - https://github.com/Tinkoff/voicekit-examples/tree/master/python
from vendors.tinkoff.python.tinkoff.cloud.stt.v1 import stt_pb2

# Импортируем наш путь до wav файла
from audio_recognition.utils.mp3_to_wav import file_wav_path

# С помощью библиотеки wave читаем файл
import wave


def build_request():
    """
    Создаем реквест с wav файлом к API тинькова
    """
    request = stt_pb2.RecognizeRequest()
    with open(file_wav_path, 'rb') as f:
        request.audio.content = f.read()
    request.config.encoding = stt_pb2.AudioEncoding.LINEAR16
    request.config.sample_rate_hertz = 44100

    """Тиньков сам не умеет определять количество каналов в файле,
       Поэтому нужна проверка каналов аудио файла, обязательная для нормального вывода текста
    """
    with wave.open(file_wav_path, 'rb') as f:
        num_channels = f.getnchannels()
    if num_channels == 1:
        request.config.num_channels = 1
    if num_channels == 2:
        request.config.num_channels = 2
    return request


def recognition_response(response):
    """Вспомогательная функция, в которой мы пробегаемся по ответу и достаем именно расшифровку слов из аудиофайла,
       ВНИМАНИЕ: Если в вашем файле больше 2 дорожек, то он не разберется на слова,
       если расшифровка не совпадает с содержимым файла, проверьте что приходит в response.result
    """
    ans_str = ''
    for result in response.results:
        for alternative in result.alternatives:
            ans_str += alternative.transcript
        return ans_str
