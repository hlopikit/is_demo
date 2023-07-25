from vendors.tinkoff.python.tinkoff.cloud.stt.v1 import stt_pb2_grpc, stt_pb2
import grpc
from vendors.tinkoff.python.auth import authorization_metadata

from django.conf import settings

from mutagen.mp3 import MP3
from pydub import AudioSegment
import wave

from django.db import models

import os


class NumberChoicesType(models.IntegerChoices):
    one = 1, 'Исходящий'
    two = 2, 'Входящий'
    three = 3, 'Входящий с перенаправлением'
    four = 4, 'Обратный'


class NumberChoicesAddToChat(models.IntegerChoices):
    zero = 0, 'Не уведомлять'
    one = 1, 'Уведомлять'



class CallInfo(models.Model):
    user_phone = models.CharField(max_length=20, null=False, blank=False)
    user_id = models.IntegerField(blank=False, null=False)
    phone_number = models.CharField(max_length=50, blank=False, null=False)
    call_date = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(null=False, blank=False,
                               choices=NumberChoicesType.choices)
    duration = models.IntegerField(null=True, blank=True)
    add_to_chat = models.IntegerField(blank=True, null=True,
                                      choices=NumberChoicesAddToChat.choices)
    call_id = models.CharField(max_length=255, null=True, blank=True)

    inner_media_path = "rings/"
    filename = ""
    file = models.FileField(upload_to=inner_media_path, null=True, blank=True)
    messages = models.TextField(blank=True, null=True)

    @staticmethod
    def recognition_response(response):
        ans_str = ''
        for result in response.results:
            for alternative in result.alternatives:
                ans_str += alternative.transcript
            return ans_str


    def telephony_externalcall_register(self, but):

        res = but.call_api_method("telephony.externalcall.register", {
            "USER_PHONE_INNER": self.user_phone,
            "USER_ID": self.user_id,
            "PHONE_NUMBER": self.phone_number,
            "CALL_START_DATE": self.call_date,
            "TYPE": self.type
        })

        self.call_id = res['result']['CALL_ID']
        self.duration = int(MP3(self.file).info.length)
        self.filename = str(self.file)[len(self.inner_media_path):-len(os.path.splitext(str(self.file))[-1])]

        self.save()

    def telephony_externalcall_finish(self, but):
        but.call_api_method('telephony.externalcall.finish', {
            "CALL_ID": self.call_id,
            "USER_ID": self.user_id,
            "DURATION": self.duration,
            "RECORD_URL": f'https://{settings.APP_SETTINGS.app_domain}/media/{self.inner_media_path}{self.filename}.mp3',
            "ADD_TO_CHAT": self.add_to_chat,
        })

    def wav_maker_n_messages(self, but):
        ne_path = os.path.join(settings.BASE_DIR, "media", self.inner_media_path, self.filename).replace(r"\\", "/")
        AudioSegment.from_mp3(f'{ne_path}.mp3').export(f'{ne_path}.wav', format="wav")

        stub = stt_pb2_grpc.SpeechToTextStub(grpc.secure_channel(settings.ENDPOINT, grpc.ssl_channel_credentials()))
        metadata = authorization_metadata(settings.API_KEY, settings.SECRET_KEY, "tinkoff.cloud.stt")
        response = stub.Recognize(self.build_request(), metadata=metadata)

        self.messages = response
        self.save()

        but.call_api_method('telephony.call.attachTranscription', {
            "CALL_ID": self.call_id,
            "MESSAGES": [{
                'SIDE': "User",
                'START_TIME': 1,
                'STOP_TIME': 3,
                'MESSAGE': self.recognition_response(self.messages)
            }]
        })

    def build_request(self):
        request = stt_pb2.RecognizeRequest()
        ne_path = os.path.join(settings.BASE_DIR, "media", self.inner_media_path, self.filename).replace(r"\\", "/")
        with open(f"{ne_path}.wav", 'rb') as f:
            request.audio.content = f.read()
        request.config.encoding = stt_pb2.AudioEncoding.LINEAR16
        request.config.sample_rate_hertz = 44100

        # Проверка каналов аудио файла, обязательна для норм. вывода текста
        with wave.open(f"{ne_path}.wav", 'rb') as f:
            num_channels = f.getnchannels()
        if num_channels == 1:
            request.config.num_channels = 1
        if num_channels == 2:
            request.config.num_channels = 2
        return request

    def __str__(self):
        return (f'Звонок на номер {self.phone_number}. '
                f'Время: {self.call_date}')
