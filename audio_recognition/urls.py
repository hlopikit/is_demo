from django.urls import path

from .views.show_html_info import show_info

urlpatterns = [
    path('show_info/', show_info, name='show_info'),
]
