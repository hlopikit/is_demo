from django.urls import path

from ones_fresh_unf_with_b24.views.company_placement import company_placement

urlpatterns = [
    path('company_placement/', company_placement),
]
