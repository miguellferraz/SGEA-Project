from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count # Import necessário para contagem de inscritos

from .models import Evento, Inscricao, Usuario
from .forms import EventForm

# Mixin de permissão para Organizadores
class OrganizadorRequiredMixin(UserPassesTestMixin):
    """
    Mixin que garante que o usuário logado tenha o perfil de 'ORGANIZADOR'.
    """
    def test_func(self):
        # Acesso permitido apenas se o usuário for staff (admin) ou tiver o perfil Organizador
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.perfil == 'ORGANIZADOR')

    def handle_no_permission(self):
        # Redireciona usuários sem permissão para a lista de eventos
        return redirect(reverse_lazy('events:event_list'))

# --- VIEWS PRINCIPAIS ---

# 1. View para Listagem de Eventos (Home Page Funcional)
class EventListView(LoginRequiredMixin, ListView):
    """Lista todos os eventos disponíveis."""
    model = Evento
    template_name = 'events/event_list.html'
    context_object_name = 'object_list'
    ordering = ['data_inicial']


# 2. View para Criação de Novo Evento (Função 2)
class EventCreateView(LoginRequiredMixin, OrganizadorRequiredMixin, CreateView):
    """Permite a criação de um novo evento, restrito a usuários 'ORGANIZADOR'."""
    model = Evento
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def form_valid(self, form):
        # Define o organizador como o usuário logado
        form.instance.organizador_responsavel = self.request.user
        return super().form_valid(form)


# 3. View para Detalhes do Evento
class EventDetailView(DetailView):
    """Exibe detalhes de um evento e o status de inscrição do usuário."""
    model = Evento
    template_name = 'events/event_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()
        user = self.request.user

        # 1. Contagem de inscritos e vagas
        inscritos_atuais = Inscricao.objects.filter(evento=evento).count()
        vagas_disponiveis = evento.qtd_participantes - inscritos_atuais
        
        context['inscritos_atuais'] = inscritos_atuais
        context['vagas_disponiveis'] = max(0, vagas_disponiveis) # Não deixa ser negativo

        # 2. Status de inscrição para o usuário logado
        context['is_inscrito'] = False
        context['is_certificado_emitido'] = False
        
        if user.is_authenticated:
            # Tenta encontrar a inscrição do usuário no evento
            inscricao = Inscricao.objects.filter(usuario=user, evento=evento).first()
            
            if inscricao:
                context['is_inscrito'] = True
                context['is_certificado_emitido'] = inscricao.certificado_emitido

        return context
    
class EventUpdateView(LoginRequiredMixin, OrganizadorRequiredMixin, UpdateView):
    """
    Permite que o organizador responsável edite um evento existente.
    """
    model = Evento
    form_class = EventForm
    template_name = 'events/event_form.html'  # Vamos reutilizar o mesmo template do formulário
    success_url = reverse_lazy('events:event_list')

    def get_queryset(self):
        # Medida de segurança: Garante que um organizador só possa editar os seus próprios eventos.
        return super().get_queryset().filter(organizador_responsavel=self.request.user)
 
# --- FUNÇÃO DE INSCRIÇÃO (Função 3) ---

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def enroll_event(request, pk):
    """Processa a inscrição do usuário logado em um evento."""
    evento = get_object_or_404(Evento, pk=pk)
    user = request.user

    # 1. Verifica se já está inscrito
    if Inscricao.objects.filter(usuario=user, evento=evento).exists():
        messages.warning(request, "Você já está inscrito neste evento.")
        return redirect('events:event_detail', pk=pk)
    
    # 2. Verifica se o usuário é organizador (não deve se inscrever)
    if user.perfil == 'ORGANIZADOR':
        messages.error(request, "Organizadores não podem se inscrever nos próprios eventos.")
        return redirect('events:event_detail', pk=pk)

    # 3. Verifica vagas
    inscritos_atuais = Inscricao.objects.filter(evento=evento).count()
    if inscritos_atuais >= evento.qtd_participantes:
        messages.error(request, "Desculpe, este evento está lotado.")
        return redirect('events:event_detail', pk=pk)

    # 4. Realiza a inscrição
    try:
        Inscricao.objects.create(usuario=user, evento=evento)
        messages.success(request, f"Inscrição realizada com sucesso no evento: {evento.tipo_evento}!")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar inscrever: {e}")

    return redirect('events:event_detail', pk=pk)

@login_required
@require_POST
def emitir_certificado(request, inscricao_id):
    """
    View para o organizador emitir um certificado para um usuário inscrito.
    """
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    evento = inscricao.evento
    
    # Garante que apenas o organizador do evento possa emitir
    if request.user != evento.organizador_responsavel:
        messages.error(request, "Você não tem permissão para emitir certificados para este evento.")
        return redirect('events:event_detail', pk=evento.pk)

    # Emite o certificado
    inscricao.certificado_emitido = True
    inscricao.save()
    
    messages.success(request, f"Certificado para {inscricao.usuario.username} emitido com sucesso!")
    return redirect('events:event_detail', pk=evento.pk)

