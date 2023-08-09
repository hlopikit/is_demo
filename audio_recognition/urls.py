from django.urls import path

from .views.show_html_info import show_info
from .views.show_info_open_ai import show_info_open_ai
from .views.upload_audio_open_ai import upload_audio_open_ai
from .views.upload_audio_tinkoff import upload_audio_tinkoff

urlpatterns = [
    path('show_info/', show_info, name='show_info'),
    path('show_info_open_ai/', show_info_open_ai, name='show_info_open_ai'),
    path('upload_audio_open_ai/', upload_audio_open_ai, name='upload_audio_open_ai'),
    path('upload_audio_tinkoff/', upload_audio_tinkoff, name='upload_audio_tinkoff'),
]
