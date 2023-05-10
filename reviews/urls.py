from django.template.context_processors import static
from django.urls import path

from FakeNews import settings
from . import views

urlpatterns = [
    path('create', views.viewForm),
    path('', views.viewForm),

]
