from django.urls import path

from allcompbizproc.views.runbizproc import run_bizproc
from crmfields.views.reload import reload_start

urlpatterns = [
    path('run_bizproc/', run_bizproc, name='run'),
    path('', reload_start, name='reload_start')
]
