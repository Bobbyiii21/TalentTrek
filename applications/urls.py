from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='applications.index'),
    path('<int:posting_id>/', views.apply, name='applications.apply'),
    path('update_status/<int:application_id>/', views.update_status, name='applications.update_status'),
]