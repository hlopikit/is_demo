from django.urls import path

from .views.employee_list import employee_list
from employeegrid.views.employee_grid import employee_grid

urlpatterns = [
    path('show_list/', employee_list),
    path('show_grid/', employee_grid)
]
