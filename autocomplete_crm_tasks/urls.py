from django.urls import path
from .views.finish_tasks_once import finish_tasks_once
from .views.initiate_auto_finish_loop import initiate_auto_finish_loop
from .views.set_flag import set_flag
from .views.get_flag import get_flag

urlpatterns = [
    path('finish_tasks/', finish_tasks_once, name='finish_tasks'),
    path('initiate_auto_finish_loop/', initiate_auto_finish_loop, name='initiate_auto_finish_loop'),
    path('set_flag/', set_flag, name='set_finish_tasks_flag'),
    path('get_flag/', get_flag, name='get_finish_tasks_flag'),

]