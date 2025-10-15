from django.db import models
from users.models import Usuario

class Evento(models.Model):
    TIPO_CHOICES = (
        ('SEMINARIO', 'Seminário'),
        ('PALESTRA', 'Palestra'),
        ('MINICURSO', 'Minicurso'),
        ('SEMANA', 'Semana Acadêmica'),
    )

    nome_evento = models.CharField(max_length=255)
    apresentador = models.CharField(max_length=255)
    tipo_evento = models.CharField(max_length=50, choices=TIPO_CHOICES)
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    local = models.CharField(max_length=255)
    qtd_participantes = models.IntegerField(default=0)
    
    organizador_responsavel = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        limit_choices_to={'perfil': 'ORGANIZADOR'} 
    )

    def __str__(self):
        return self.nome_evento

class Inscricao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    certificado_emitido = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('usuario', 'evento')

    def __str__(self):
        return f"Inscrição de {self.usuario.username} em {self.evento.tipo_evento}"