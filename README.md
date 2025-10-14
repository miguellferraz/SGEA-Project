# SGEA - Sistema de Gestão de Eventos Acadêmicos

Este projeto é um sistema web desenvolvido em Django para gerenciar eventos acadêmicos, como parte da avaliação da disciplina de [Nome da Disciplina].

## Funcionalidades Principais

- **Cadastro e Autenticação de Usuários:** Perfis de Aluno, Professor e Organizador.
- **Criação de Eventos:** Organizadores podem criar e gerenciar eventos.
- **Inscrição em Eventos:** Alunos e professores podem se inscrever nos eventos disponíveis.
- **Emissão de Certificados:** Organizadores podem emitir certificados para os participantes.

## Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://www.youtube.com/watch?v=xtwls2XmJUI](https://www.youtube.com/watch?v=xtwls2XmJUI)
    cd sgea-project
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install Django
    ```

4.  **Aplique as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```

5.  **Crie um superusuário (administrador):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Execute o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

Acesse o sistema em `http://127.0.0.1:8000`.