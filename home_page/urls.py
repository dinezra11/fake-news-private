from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('', views.home, name='home'),
    path('myProfile', views.myProfile, name='myProfile'),
    path('myarticle', views.myarticle, name='myarticle'),
]
