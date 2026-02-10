from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='posting.index'),
    path('create', views.create, name='posting.create'),
    path('explore', views.explore, name='posting.explore'),
]