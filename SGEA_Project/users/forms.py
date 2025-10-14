from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # Usa o modelo Usuario personalizado
        model = Usuario
        # Inclui os campos padrão necessários e os campos personalizados
        fields = (
            'username', 
            'email', 
            'first_name', 
            'telefone', 
            'instituicao_ensino', 
            'perfil'
        )
        # Define rótulos amigáveis para alguns campos
        labels = {
            'username': 'Nome de Usuário (Login)',
            'email': 'E-mail (Opcional)',
            'first_name': 'Nome Completo',
        }

    # Você pode adicionar lógica de validação aqui, se necessário.
    # Por exemplo, garantir que 'instituicao_ensino' seja preenchido se o perfil for ALUNO ou PROFESSOR.
    def clean(self):
        cleaned_data = super().clean()
        perfil = cleaned_data.get("perfil")
        instituicao = cleaned_data.get("instituicao_ensino")

        if perfil in ['ALUNO', 'PROFESSOR'] and not instituicao:
            self.add_error('instituicao_ensino', 'Este campo é obrigatório para perfis de Aluno ou Professor.')
        
        return cleaned_data
