from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UsuarioRegisterView

urlpatterns = [
    path('cadastro/', UsuarioRegisterView.as_view(), name='register'),
    
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        next_page='/eventos/'  
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
    ), name='logout'),
]