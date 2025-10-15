from django import forms
from .models import Evento

class EventForm(forms.ModelForm):
    
    class Meta:
        model = Evento
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
        
        widgets = {
            'nome_evento': forms.TextInput(attrs={'placeholder': 'Ex: Semana da Computação'}),
            'apresentador': forms.TextInput(attrs={'placeholder': 'Ex: Dr. Fulano de Tal'}),
            'data': forms.DateInput(attrs={'type': 'date'}),
            'horario_inicio': forms.TimeInput(attrs={'type': 'time'}), # Alterado
            'horario_fim': forms.TimeInput(attrs={'type': 'time'}),
        }