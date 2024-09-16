# explore/urls.py

from django.urls import path
from . import views
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #path('', lambda request: redirect('home')),  # Redirect root URL to /home/
    path('', views.home, name='home'),  # Home page
    path('category/<str:category>/', views.subcategories, name='subcategories'),
    path('discovery/', views.discovery, name='discovery'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),
]
