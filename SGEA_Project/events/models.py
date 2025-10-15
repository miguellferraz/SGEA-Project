from django.db import models
from users.models import Usuario # Importa seu Custom User Model

# 1. Modelo Evento
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
    
    # FK para o Organizador (relaciona com o modelo Usuario no app 'users')
    organizador_responsavel = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        limit_choices_to={'perfil': 'ORGANIZADOR'} # Garante que apenas organizadores possam ser selecionados
    )

    def __str__(self):
        return self.nome_evento

# 2. Modelo Inscrição (Tabela M:N)
class Inscricao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    certificado_emitido = models.BooleanField(default=False)
    
    # Garante que um usuário só possa se inscrever uma vez por evento
    class Meta:
        unique_together = ('usuario', 'evento')

    def __str__(self):
        return f"Inscrição de {self.usuario.username} em {self.evento.tipo_evento}"