from callsuploader.utils.python.tinkoff.cloud.stt.v1 import stt_pb2_grpc, stt_pb2
import grpc
from callsuploader.utils.python.auth import authorization_metadata
from _local_settings import ENDPOINT, API_KEY, SECRET_KEY

from pydub import AudioSegment

#  ВНИМАНИЕ МЫ РАБОТАЕМ С ffmpeg!!! Его надо установить на пк так -

src = 'В 1712 году столица.mp3'
dst = 'test.wav'
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")


def build_request():
    request = stt_pb2.RecognizeRequest()
    with open("test_file.wav", "rb") as f:
        request.audio.content = f.read()
    request.config.encoding = stt_pb2.AudioEncoding.LINEAR16
    request.config.sample_rate_hertz = 44100  # Значение не содержится в файле ".s16"
    request.config.num_channels = 1  # Значение не содержится в файле ".s16"
    return request


def print_recognition_response(response):
    for result in response.results:
        print("Channel", result.channel)
        print("Phrase start:", result.start_time.ToTimedelta())
        print("Phrase end:  ", result.end_time.ToTimedelta())
        for alternative in result.alternatives:
            print('"' + alternative.transcript + '"')
        print("----------------------------")


stub = stt_pb2_grpc.SpeechToTextStub(grpc.secure_channel(ENDPOINT, grpc.ssl_channel_credentials()))
metadata = authorization_metadata(API_KEY, SECRET_KEY, "tinkoff.cloud.stt")
response = stub.Recognize(build_request(), metadata=metadata)
print_recognition_response(response)
