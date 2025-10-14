from django.shortcuts import render

def index(request):
    """Renderiza a página inicial (Home Page) do SGEA."""
    # Note que você deve criar o template em: inicio/templates/inicio/index.html
    return render(request, 'inicio/index.html', {
        'title': 'Bem-vindo ao SGEA',
        'is_authenticated': request.user.is_authenticated # Envia status de login
    })
