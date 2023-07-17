from django.urls import path

from company_on_map.views.company_on_map_view import company_on_map

urlpatterns = [
    path('map/', company_on_map, name="company_on_map"),
]
