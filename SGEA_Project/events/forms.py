from django import forms
from .models import Evento

class EventForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        # Apenas os campos preenchidos pelo usuário são listados.
        # 'organizador_responsavel' será preenchido automaticamente na View.
        fields = [
            'nome_evento', 
            'apresentador',    
            'tipo_evento', 
            'data',
            'horario_inicio',
            'horario_fim',  
            'local', 
            'qtd_participantes'
        ]
        
        # Adiciona widgets para melhor UX no HTML (Ex: DateField usa um seletor de data)
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario_inicio': forms.TimeInput(attrs={'type': 'time'}), # Alterado
            'horario_fim': forms.TimeInput(attrs={'type': 'time'}),
        }