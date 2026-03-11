from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('notifications', views.notifications, name='home.notifications'),
    path('notification_click/<int:id>', views.notification_click, name='home.notification_click'),
]