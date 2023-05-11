
from django.template.context_processors import static
from django.urls import path

from FakeNews import settings
from . import views

urlpatterns = [

path('graphPredictionapprovess', views.graphPredictionapprovess, name='graphPredictionapprovess'),

]
