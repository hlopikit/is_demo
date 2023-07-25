# Импортируем нужные нам файлы из папки тинькова
from vendors.tinkoff.python.tinkoff.cloud.stt.v1 import stt_pb2_grpc
from vendors.tinkoff.python.auth import authorization_metadata
import grpc

# Импортируем промежуточные функции из utils
from audio_recognition.utils.mp3_to_wav import wav_maker
from audio_recognition.utils.build_n_get import build_request, recognition_response

# Нужные ключи мы получили тут - https://software.tinkoff.ru/account/voicekit/keys/ и положили их в local_settings
from _local_settings import ENDPOINT, API_KEY, SECRET_KEY


def get_text():
    """Для начала вызываем wav_maker, для того чтобы переделать mp3 в понятный для тинькова wav,
       после уже по файлу wav мы запускаем функции распознавания голоса, ответ выводим через
       вспомогательную функцию recognition_response
    """
    wav_maker()
    stub = stt_pb2_grpc.SpeechToTextStub(grpc.secure_channel(ENDPOINT, grpc.ssl_channel_credentials()))
    metadata = authorization_metadata(API_KEY, SECRET_KEY, "tinkoff.cloud.stt")
    """Метод "Recognize" работает по принципу "загружаем аудио целиком -
       получаем ответ", полезен для распознавания аудиофайлов,
       остальные методы можно посмотреть тут - https://software.tinkoff.ru/docs/voicekit/stttutorial/
     """
    response = stub.Recognize(build_request(), metadata=metadata)
    # print(recognition_response(response))  Раскоментить для теста через print
    return recognition_response(response)


# print(get_text())
