from django.urls import path
from .views.export_calls import export_calls
from .views.keep_synced import keep_synced
from .views.get_flag import get_flag
from .views.set_flag import set_flag

urlpatterns = [
    path('send_call_info/', export_calls, name='export_calls'),
    path('keep_synced/', keep_synced, name='keep_synced'),
    path('get_flag/', get_flag, name='get_call_sync_flag'),
    path('set_flag/', set_flag, name='set_call_sync_flag'),
]