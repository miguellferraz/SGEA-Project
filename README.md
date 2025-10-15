# SGEA - Sistema de Gestão de Eventos Acadêmicos

O SGEA é um sistema web completo desenvolvido em Django para o gerenciamento de eventos acadêmicos, como seminários, palestras e minicursos. O projeto foi criado como parte da avaliação da disciplina de Programação para Web.

## ✨ Funcionalidades Principais

- **Autenticação de Usuários:** Sistema completo de cadastro, login e logout com perfis distintos (Aluno, Professor, Organizador).
- **Gerenciamento de Eventos:** Organizadores podem criar, listar, buscar, editar e gerenciar todos os aspectos dos eventos.
- **Páginas Personalizadas:**
    - **Organizadores:** Visualizam uma página com apenas os eventos que criaram ("Meus Eventos").
    - **Alunos/Professores:** Acessam uma página com todas as suas inscrições ("Minhas Inscrições").
- **Sistema de Inscrição:** Alunos e professores podem se inscrever em eventos, com validação de vagas e perfis.
- **Emissão de Certificados em PDF:** Geração automática de certificados em PDF com design profissional, para os participantes.
- **Busca Inteligente:** Funcionalidade de busca que filtra eventos por nome, apresentador ou tipo.

## 🚀 Tecnologias Utilizadas

- **Backend:** Python com o framework Django.
- **Frontend:** HTML5, TailwindCSS para estilização e JavaScript para funcionalidades dinâmicas (máscara de formulário).
- **Banco de Dados:** SQLite 3 (padrão do Django para desenvolvimento).
- **Geração de PDF:** Biblioteca `reportlab` com `Pillow`.

## ⚙️ Como Executar o Projeto Localmente

Siga os passos abaixo para rodar o projeto em seu ambiente de desenvolvimento.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/miguellferraz/SGEA-Project](https://github.com/miguellferraz/SGEA-Project)
    cd SGEA-Project
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # No Windows
    python -m venv venv
    venv\Scripts\activate

    # No macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    Use o gerenciador de pacotes `pip` para instalar todas as bibliotecas listadas no `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplique as migrações do banco de dados:**
    Este comando cria o arquivo de banco de dados `db.sqlite3` e todas as tabelas necessárias.
    ```bash
    python manage.py migrate
    ```

5.  **Crie um superusuário (administrador):**
    Você precisará de um superusuário para acessar a área administrativa do Django (`/admin/`).
    ```bash
    python manage.py createsuperuser
    ```

6.  **Execute o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

O sistema estará disponível em `http://127.0.0.1:8000`.