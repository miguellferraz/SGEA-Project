from django.urls import path
from . import views

# Define o namespace
app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('criar/', views.EventCreateView.as_view(), name='event_create'),
    path('meus-eventos/', views.MyEventListView.as_view(), name='my_event_list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/editar/', views.EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/inscrever/', views.enroll_event, name='enroll_event'),
    path('inscricao/<int:inscricao_id>/emitir_certificado/', views.emitir_certificado, name='emitir_certificado'),
]