# explore/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('category/<str:category>/', views.subcategories, name='subcategories'),
    path('discovery/', views.discovery, name='discovery'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
]
