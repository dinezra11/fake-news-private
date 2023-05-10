from django.template.context_processors import static
from django.urls import path

from FakeNews import settings
from . import views

urlpatterns = [
    path('login', views.Login, name='login'),
    path('register', views.register_user, name='register'),
    path('logout2', views.logout2, name='logout2'),
]
