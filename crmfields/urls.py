from django.urls import path

from crmfields.views.show_lead_fields import show_lead_fields
from .views.show_contact_fields import show_contact_fields
from .views.show_deal_fields import show_deal_fields
from .views.reload import reload_start

urlpatterns = [
    path('show_lead_fields/', show_lead_fields),
    path('show_contact_fields/', show_contact_fields),
    path('show_deal_fields/', show_deal_fields),
    path('', reload_start, name='reload_start')
]
