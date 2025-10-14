from django.urls import path
from . import views

# O namespace (app_name) é opcional mas recomendado
app_name = 'inicio' 

urlpatterns = [
    # Mapeia o caminho VAZIO ('') para a view index.
    path('', views.index, name='home'),
]
