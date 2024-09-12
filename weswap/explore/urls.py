# explore/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('category/<str:category>/', views.subcategories, name='subcategories'),
]
