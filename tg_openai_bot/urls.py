from django.urls import path

from tg_openai_bot.views.start_page import start_page_open_ai

urlpatterns = [
    path('open_ai/', start_page_open_ai, name='start_page_for_open_ai'),
    ]
