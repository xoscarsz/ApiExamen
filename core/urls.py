from django.urls import path
from api.views import home, tarea_preparacion, tarea_entrenamiento, tarea_evaluacion

urlpatterns = [
    path('', home, name='home'), # La página principal
    path('preparar/', tarea_preparacion, name='preparar'),
    path('entrenar/', tarea_entrenamiento, name='entrenar'),
    path('evaluar/', tarea_evaluacion, name='evaluar'),
]