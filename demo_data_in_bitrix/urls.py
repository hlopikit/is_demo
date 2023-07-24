import settings
from django.urls import path
from django.conf.urls.static import static

from .views.demo_data_form import demo_data_form
from .views.load_from_googledocs import load_from_googledocs

urlpatterns = [
                  path('demo_data_form/', demo_data_form, name='demo_data_form'),
                  path('load_from_googledocs/', load_from_googledocs, name='load_from_googledocs'),
              ]
