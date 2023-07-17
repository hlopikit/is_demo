from django.urls import path

from crmfields.views.reload import reload_start
from employeegrid.views.employee_grid import employee_grid

urlpatterns = [
    path('show_grid/', employee_grid),
    path('reload_start/', reload_start)
]