from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='accounts.index'),
    path('register', views.register, name='accounts.register'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('onboard/', views.onboard, name='accounts.onboard'),
    path('<str:user_link>/', views.profiles, name='accounts.profiles'),
]