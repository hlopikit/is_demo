import settings
from django.urls import path
from django.conf.urls.static import static

from .views.export_deals_view import export_deals

urlpatterns = [
                  path('export_deals/', export_deals, name='export_deals'),
              ]
