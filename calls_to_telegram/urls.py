from django.urls import path
from .views.export_calls import export_calls
from .views.keep_synced import keep_synced

urlpatterns = [
    path('send_call_info/', export_calls, name='export_calls'),
    path('keep_synced/', keep_synced, name='keep_synced'),
]