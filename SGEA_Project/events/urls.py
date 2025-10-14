from django.urls import path
from . import views

# Define o namespace
app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('criar/', views.EventCreateView.as_view(), name='event_create'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:pk>/inscrever/', views.enroll_event, name='enroll_event'),
]