
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    #path('login/',views.user_login, name='login'),
    path('login/',auth_view.LoginView.as_view(),name='login'),
    path('logout/',auth_view.LogoutView.as_view(),name='logout'),
    path('',views.dashboard, name='dashboard'),
]