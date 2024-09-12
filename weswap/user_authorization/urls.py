from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('password_reset/', views.password_reset, name='password_reset'),
]
