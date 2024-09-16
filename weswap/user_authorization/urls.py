from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('change_password/', views.change_password, name='change_password'),
]
