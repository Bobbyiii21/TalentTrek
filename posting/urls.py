from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='posting.index'),
    path('<int:id>/', views.post, name='posting.post'),
]