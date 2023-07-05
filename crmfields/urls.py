from django.urls import path

import settings
from crmfields.views.show_company_fields import show_company_fields
from crmfields.views.show_lead_fields import show_lead_fields
from crmfields.views.reload import reload_start
from django.conf.urls.static import static

urlpatterns = [
    path('show_lead_fields/', show_lead_fields),
    path('show_company_fields/', show_company_fields, ),
    path('', reload_start, name='reload_start')
]
