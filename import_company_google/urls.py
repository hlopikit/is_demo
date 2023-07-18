from django.urls import path

from crmfields.views.show_lead_fields import show_lead_fields
from import_company_google.views.import_company_view import import_company_google

urlpatterns = [
    path('import/', import_company_google, name="import_company_google"),
]
