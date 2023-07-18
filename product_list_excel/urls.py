from django.urls import path

from .views.excel_product import product_in_excel


urlpatterns = [
    path('product_excel/', product_in_excel, name='product_in_excel'),
]
