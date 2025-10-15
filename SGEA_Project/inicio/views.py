from django.shortcuts import render

def index(request):
    return render(request, 'inicio/index.html', {
        'title': 'Bem-vindo ao SGEA',
        'is_authenticated': request.user.is_authenticated 
    })
