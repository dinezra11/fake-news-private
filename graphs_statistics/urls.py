
from django.template.context_processors import static
from django.urls import path

from FakeNews import settings
from . import views

urlpatterns = [
    path('graph', views.graphPredictionapprovess, name='graph'),
    path('general', views.graphGeneral, name='general_graphs'),
]
