from django.urls import path
from .views.index import index
from .views.move_button import move_button
from .views.bind_button import bind_button
from .views.unbind_button import unbind_button


app_name = 'move_tasks_deadline_js'
urlpatterns = [
    path('', index, name='index'),
    path('move_button', move_button, name='move_button'),
    path('bind_button', bind_button, name='bind_button'),
    path('unbind_button', unbind_button, name='unbind_button'),
]
