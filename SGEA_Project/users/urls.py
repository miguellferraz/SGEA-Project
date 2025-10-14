from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UsuarioRegisterView

urlpatterns = [
    # Funcionalidade 1: Cadastro de Usuários
    path('cadastro/', UsuarioRegisterView.as_view(), name='register'),
    
    # Funcionalidade 2: Autenticação de Usuários (Login)
    # Usa a view nativa do Django. Redireciona para a Home Page após login.
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        next_page='/' # Redireciona para a raiz após login (será a Home/Eventos)
    ), name='login'),
    
    # Funcionalidade 2: Autenticação de Usuários (Logout)
    # Redireciona para a página de login após logout
    path('logout/', auth_views.LogoutView.as_view(
        next_page='/'
    ), name='logout'),
]