from django.urls import path

from .views.export_deals_view import export_deals
from .views.entrance import entrance

urlpatterns = [
                  path('export_deals/', export_deals, name='export_deals'),
                  path('entrance/', entrance),
              ]
