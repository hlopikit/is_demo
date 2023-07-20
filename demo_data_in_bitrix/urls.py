import settings
from django.urls import path
from django.conf.urls.static import static

from .views.demo_data import excel

urlpatterns = [
                  path('excel/', excel, name='excel'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
