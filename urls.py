"""fitness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import settings
from django.contrib import admin
from django.urls import path, include
from post_currency.views import *
from django.conf.urls.static import static

from start.views.start import start

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', start),
    path('tasks/', include('tasks.urls')),
    path('ones/', include('ones_fresh_unf_with_b24.urls')),
    path('crmfields/', include('crmfields.urls')),
    path('contactmp3/', include('contactmp3.urls')),
    path('duplicatefinder/', include('duplicatefinder.urls')),
    path('urlmanager/', include('usermanager.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
