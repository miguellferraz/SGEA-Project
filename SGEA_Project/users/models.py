from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # O AbstractUser já fornece: username, password, first_name, last_name, email, is_active, etc.

    telefone = models.CharField(max_length=15, verbose_name='Telefone', blank=True, null=True)

    # Requisito: instituição de ensino (alunos e professores obrigatório)
    instituicao_ensino = models.CharField(
        max_length=100, 
        verbose_name='Instituição de Ensino', 
        blank=True, 
        null=True
    )

    # Perfil (aluno, professor, organizador)
    PERFIL_CHOICES = (
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('ORGANIZADOR', 'Organizador'),
    )
    perfil = models.CharField(
        max_length=15,
        choices=PERFIL_CHOICES,
        default='ALUNO',
        verbose_name='Perfil'
    )
    
    # Adiciona a data de registro, útil para auditoria
    data_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username
