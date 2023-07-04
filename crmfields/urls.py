from django.urls import path

from crmfields.views.show_lead_fields import show_lead_fields

urlpatterns = [
    path('show_lead_fields/', show_lead_fields),
]
