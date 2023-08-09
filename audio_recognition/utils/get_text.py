# Импортируем нужные нам файлы из папки тинькова
from vendors.tinkoff.python.tinkoff.cloud.stt.v1 import stt_pb2_grpc
from vendors.tinkoff.python.auth import authorization_metadata
import grpc

# Импортируем промежуточные функции из utils
from audio_recognition.utils.mp3_to_wav import wav_maker
from audio_recognition.utils.build_n_get import build_request, recognition_response

# Нужные ключи мы получили тут - https://software.tinkoff.ru/account/voicekit/keys/ и положили их в local_settings
from django.conf import settings


def get_text(filename="file_for_test.mp3"):
    """Для начала вызываем wav_maker, для того чтобы переделать mp3 в понятный для тинькова wav,
       после уже по файлу wav мы запускаем функции распознавания голоса, ответ выводим через
       вспомогательную функцию recognition_response
    """
    file_path = wav_maker(filename)
    stub = stt_pb2_grpc.SpeechToTextStub(grpc.secure_channel(settings.ENDPOINT_TINKOFF,
                                                             grpc.ssl_channel_credentials()))
    metadata = authorization_metadata(settings.TINKOFF_API_KEY, settings.SECRET_KEY_TINKOFF, "tinkoff.cloud.stt")
    """Метод "Recognize" работает по принципу "загружаем аудио целиком -
       получаем ответ", полезен для распознавания аудиофайлов,
       остальные методы можно посмотреть тут - https://software.tinkoff.ru/docs/voicekit/stttutorial/
     """
    response = stub.Recognize(build_request(file_path), metadata=metadata)
    # print(recognition_response(response))  Раскоментить для теста через print
    return recognition_response(response)
