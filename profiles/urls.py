from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='profiles.register'),
    path('login/', views.login, name='profiles.login'),
    path('logout/', views.logout, name='profiles.logout'),
    path('onboard/', views.onboard, name='profiles.onboard'),
    path('', views.index, name='profiles.index'),
]