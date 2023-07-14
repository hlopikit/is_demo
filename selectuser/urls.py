from django.urls import path

from .views.selectuser import select_user

urlpatterns = [
    path('SelectUser/', select_user, name='select_user'),
]