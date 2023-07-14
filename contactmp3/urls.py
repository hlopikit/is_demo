from django.urls import path

from .views.register_call import reg_call

urlpatterns = [
    path('register_call/', reg_call, name='register_call'),
]
