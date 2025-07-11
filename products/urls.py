
# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('clothing-styles/', views.clothing_styles_api, name='clothing_styles_api'),
]