from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='profiles.index'),
<<<<<<< HEAD
    #path('about', views.about, name='home.about'),
=======
>>>>>>> setup_wizard
]