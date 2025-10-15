from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Evento, Inscricao, Usuario
from .forms import EventForm

# Mixin de permissão para Organizadores
class OrganizadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.perfil == 'ORGANIZADOR')

    def handle_no_permission(self):
        return redirect(reverse_lazy('events:event_list'))

# --- VIEWS PRINCIPAIS ---

class EventListView(ListView):
    model = Evento
    template_name = 'events/event_list.html'
    context_object_name = 'object_list'
    ordering = ['data']  # CORRIGIDO AQUI

class MyEventListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'events/event_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Evento.objects.filter(organizador_responsavel=self.request.user).order_by('data') # CORRIGIDO AQUI

class EventCreateView(LoginRequiredMixin, OrganizadorRequiredMixin, CreateView):
    model = Evento
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def form_valid(self, form):
        form.instance.organizador_responsavel = self.request.user
        return super().form_valid(form)

class EventDetailView(LoginRequiredMixin, DetailView):
    model = Evento
    template_name = 'events/event_detail.html'
    context_object_name = 'object'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = self.get_object()
        user = self.request.user
        inscritos_atuais = Inscricao.objects.filter(evento=evento).count()
        vagas_disponiveis = evento.qtd_participantes - inscritos_atuais
        context['inscritos_atuais'] = inscritos_atuais
        context['vagas_disponiveis'] = max(0, vagas_disponiveis)
        context['is_inscrito'] = False
        context['is_certificado_emitido'] = False
        if user.is_authenticated:
            inscricao = Inscricao.objects.filter(usuario=user, evento=evento).first()
            if inscricao:
                context['is_inscrito'] = True
                context['is_certificado_emitido'] = inscricao.certificado_emitido
        return context

class EventUpdateView(LoginRequiredMixin, OrganizadorRequiredMixin, UpdateView):
    model = Evento
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('events:event_list')

    def get_queryset(self):
        return super().get_queryset().filter(organizador_responsavel=self.request.user)

class MyInscriptionsListView(LoginRequiredMixin, ListView):
    """
    Lista os eventos nos quais o usuário (aluno/professor) está inscrito.
    """
    model = Inscricao  # O modelo principal agora é a Inscrição
    template_name = 'events/my_inscriptions.html'
    context_object_name = 'inscricoes_list'

    def get_queryset(self):
        # Filtra as inscrições para pegar apenas as do usuário logado e ordena pela data do evento
        return Inscricao.objects.filter(usuario=self.request.user).order_by('evento__data')
    
# --- FUNÇÕES AUXILIARES ---

@login_required
@require_POST
def enroll_event(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    user = request.user
    if Inscricao.objects.filter(usuario=user, evento=evento).exists():
        messages.warning(request, "Você já está inscrito neste evento.")
        return redirect('events:event_detail', pk=pk)
    if user.get_full_name() == evento.apresentador:
        messages.error(request, "Você é o apresentador e não pode se inscrever no próprio evento.")
        return redirect('events:event_detail', pk=pk)
    if user.perfil == 'ORGANIZADOR':
        messages.error(request, "Organizadores não podem se inscrever nos próprios eventos.")
        return redirect('events:event_detail', pk=pk)
    inscritos_atuais = Inscricao.objects.filter(evento=evento).count()
    if inscritos_atuais >= evento.qtd_participantes:
        messages.error(request, "Desculpe, este evento está lotado.")
        return redirect('events:event_detail', pk=pk)
    try:
        Inscricao.objects.create(usuario=user, evento=evento)
        messages.success(request, f"Inscrição realizada com sucesso no evento: {evento.nome_evento}!")
    except Exception as e:
        messages.error(request, f"Ocorreu um erro ao tentar inscrever: {e}")
    return redirect('events:event_detail', pk=pk)

@login_required
@require_POST
def emitir_certificado(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    evento = inscricao.evento
    if request.user != evento.organizador_responsavel:
        messages.error(request, "Você não tem permissão para emitir certificados para este evento.")
        return redirect('events:event_detail', pk=evento.pk)
    inscricao.certificado_emitido = True
    inscricao.save()
    messages.success(request, f"Certificado para {inscricao.usuario.username} emitido com sucesso!")
    return redirect('events:event_detail', pk=evento.pk)