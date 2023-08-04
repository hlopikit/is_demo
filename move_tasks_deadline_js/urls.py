from django.urls import path
from .views import move_tasks_deadline_js


app_name = 'move_tasks_deadline_js'
urlpatterns = [
    path('', move_tasks_deadline_js.index, name='index'),
]