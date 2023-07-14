from django.urls import path

from crmfields.views.reload import reload_start
from duplicatefinder.views.find_duplicate import find_duplicates

urlpatterns = [
    path('finded_duplicates/', find_duplicates),
    path('', reload_start, name='reload_start'),
]
