from django.urls import path

from tg_openai_bot.views.start_page import start_page_open_ai
from tg_openai_bot.views.start_page_stand_alone import start_page_open_ai_stand_alone

urlpatterns = [
    path('open_ai/', start_page_open_ai, name='start_page_for_open_ai'),
    path('open_ai/', start_page_open_ai_stand_alone, name='start_page_for_open_ai')
    ]
