from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from .models import Usuario

# 1. View para Cadastro de Novos Usuários
class UsuarioRegisterView(CreateView):
    model = Usuario
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    
    # Redireciona o usuário para a página de login após o cadastro
    success_url = reverse_lazy('login') 
    
    # Contexto para a página de prototipação
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cadastro de Novo Usuário'
        return context
