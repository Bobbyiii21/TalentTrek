from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='applications.index'),
    path('<str:view_mode>/', views.index, name='applications.index'),
    path('apply/<int:posting_id>/', views.apply, name='applications.apply'),
    path('update_status/<int:application_id>/<str:context>', views.update_status, name='applications.update_status'),
]
