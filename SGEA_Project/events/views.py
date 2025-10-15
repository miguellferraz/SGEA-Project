from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
import os
from django.conf import settings

from .models import Evento, Inscricao, Usuario
from .forms import EventForm

class OrganizadorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.perfil == 'ORGANIZADOR')
    def handle_no_permission(self):
        return redirect(reverse_lazy('events:event_list'))

class EventListView(ListView):
    model = Evento
    template_name = 'events/event_list.html'
    context_object_name = 'object_list'
    def get_queryset(self):
        queryset = Evento.objects.all().order_by('data')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nome_evento__icontains=query) | Q(apresentador__icontains=query) | Q(tipo_evento__icontains=query)).distinct()
        return queryset

class MyEventListView(LoginRequiredMixin, ListView):
    model = Evento
    template_name = 'events/event_list.html'
    context_object_name = 'object_list'
    def get_queryset(self):
        queryset = Evento.objects.filter(organizador_responsavel=self.request.user).order_by('data')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nome_evento__icontains=query) | Q(apresentador__icontains=query) | Q(tipo_evento__icontains=query)).distinct()
        return queryset

class MyInscriptionsListView(LoginRequiredMixin, ListView):
    model = Inscricao
    template_name = 'events/my_inscriptions.html'
    context_object_name = 'inscricoes_list'
    def get_queryset(self):
        return Inscricao.objects.filter(usuario=self.request.user).order_by('evento__data')

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
            context['inscricao'] = inscricao  # <-- PEQUENA ADIÇÃO AQUI
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
        messages.error(request, "Organizadores não podem se inscrever em eventos.")
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

# --- NOVA VIEW DE GERAÇÃO DE PDF ---
@login_required
def generate_certificate_pdf(request, inscricao_id):
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)

    if not inscricao.certificado_emitido:
        messages.error(request, "Este certificado ainda não foi emitido.")
        return redirect('events:my_inscriptions')
    if request.user != inscricao.usuario and request.user != inscricao.evento.organizador_responsavel:
        messages.error(request, "Você não tem permissão para baixar este certificado.")
        return redirect('events:my_inscriptions')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.setFillColor(colors.darkblue)

    logo_path = os.path.join(settings.BASE_DIR, 'sgea_core', 'static', 'images', 'logo.png')
    try:
        p.drawImage(logo_path, width / 2 - 0.5 * inch, height - 1.5 * inch, width=1*inch, height=1*inch, mask='auto')
    except:
        pass

    p.setFont("Helvetica-Bold", 36)
    p.drawCentredString(width / 2.0, height - 2.5 * inch, "Certificado")

    # Linha decorativa
    p.setStrokeColor(colors.lightgrey)
    p.setLineWidth(2)
    p.line(1.5 * inch, height - 2.7 * inch, width - 1.5 * inch, height - 2.7 * inch)

    # Corpo do Texto com Quebra de Linha Automática (usando Paragraph)
    styles = getSampleStyleSheet()
    style_body = ParagraphStyle(
        'body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=22,
        alignment=1,  # 0=Left, 1=Center, 2=Right
    )

    aluno_nome = inscricao.usuario.get_full_name() or inscricao.usuario.username
    evento_nome = inscricao.evento.nome_evento
    evento_data = inscricao.evento.data.strftime('%d de %B de %Y') # Formato de data mais elegante

    text = f"""
        Certificamos que <b>{aluno_nome}</b> participou do evento
        <br/><br/>
        <b>"{evento_nome}"</b>
        <br/><br/>
        realizado em {evento_data}.
    """

    p_text = Paragraph(text, style_body)
    p_text.wrapOn(p, width - 3 * inch, height) # Define a área do parágrafo
    p_text.drawOn(p, 1.5 * inch, height - 5 * inch) # Desenha o parágrafo

    # Assinatura (simulada)
    p.setFont("Helvetica-Oblique", 12)
    p.drawCentredString(width / 2.0, 2 * inch, "_________________________")
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2.0, 1.8 * inch, "SGEA - Organização de Eventos")

    # Rodapé
    p.setFont("Helvetica", 9)
    p.setFillColor(colors.grey)
    p.drawCentredString(width / 2.0, 0.5 * inch, f"ID do Certificado: {inscricao.id}-{inscricao.evento.id}-{inscricao.usuario.id}")

    # --- FIM DA ESTILIZAÇÃO ---

    p.showPage()
    p.save()

    buffer.seek(0)
    filename = f"certificado-{aluno_nome.replace(' ', '-')}-{evento_nome.replace(' ', '-')}.pdf"
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    return response