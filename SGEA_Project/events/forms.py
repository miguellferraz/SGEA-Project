from django import forms
from .models import Evento

class EventForm(forms.ModelForm):
    
    class Meta:
        model = Evento
        # Apenas os campos preenchidos pelo usuário são listados.
        # 'organizador_responsavel' será preenchido automaticamente na View.
        fields = [
            'tipo_evento', 
            'data_inicial', 
            'data_final', 
            'horario', 
            'local', 
            'qtd_participantes'
        ]
        
        # Adiciona widgets para melhor UX no HTML (Ex: DateField usa um seletor de data)
        widgets = {
            'data_inicial': forms.DateInput(attrs={'type': 'date'}),
            'data_final': forms.DateInput(attrs={'type': 'date'}),
            'horario': forms.TimeInput(attrs={'type': 'time'}),
        }