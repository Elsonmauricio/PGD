from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)  # Criação da instância do Flask

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html', title="Página Inicial", message="Bem-vindo ao PGD!")

# Dados simulados
clientes = {
    1: {"nome": "João Silva", "email": "joao@email.com", "data_criacao": "2025-01-01"},
    2: {"nome": "Maria Oliveira", "email": "maria@email.com", "data_criacao": "2025-01-10"}
}

@app.route('/profile')
def profile():
    # Substitua pelos dados reais do usuário
    
    return render_template('profile.html')

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Lógica de validação do login (pode ser implementada conforme necessário)
        # Exemplo de verificação no banco de dados
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.password == password:
            return redirect(url_for('index'))  # Redirecionando para a página inicial após o login
        else:
            return render_template('login.html', title="Login", error="Email ou senha inválidos")

    # Se o método for GET (ou seja, a página é acessada inicialmente), renderize o HTML do login
    return render_template('login.html', title="Login")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtenha os dados do formulário
        name = request.form['name']
        email = request.form['signup_email']
        password = request.form['signup_password']
        confirm_password = request.form['confirm_password']

        # Validação simples (exemplo)
        if password != confirm_password:
            return render_template('register.html', title="Register", error="Passwords do not match.")
        
        # Salvar os dados no banco de dados
        novo_usuario = Usuario(name=name, email=email, password=password)
        db.session.add(novo_usuario)
        db.session.commit()

        # Redirecionar após o cadastro
        return redirect(url_for('login'))

    # Renderiza o formulário caso seja um método GET
    return render_template('register.html', title="Register")

# Função de cadastro de desempregado (atualizada)
@app.route('/cadastrar_desempregado', methods=['GET', 'POST'])
def cadastrar_desempregado():
    if request.method == 'POST':
        # Lógica para processar o formulário
        nome = request.form['nome']
        habilidades = request.form['habilidades']
        experiencia = request.form['experiencia']
        formacao = request.form['formacao']
        contato = request.form['contato']
        curriculo = request.form['curriculo']
        
        # Adiciona o desempregado à lista
        desempregados.append({
            'nome': nome,
            'habilidades': habilidades.split(', '),
            'experiencia': experiencia,
            'formacao': formacao,
            'contato': contato,
            'curriculo': curriculo
        })
        # Usar o nome como ID para redirecionar
        return redirect(url_for('area_desempregado', desempregado_id=nome))  # Redireciona para a área do desempregado

    # Renderiza o formulário
    form = {
        'fields': [
            {'label': 'Nome', 'name': 'nome', 'id': 'nome', 'type': 'text'},
            {'label': 'Habilidades (separadas por vírgula)', 'name': 'habilidades', 'id': 'habilidades', 'type': 'text'},
            {'label': 'Experiência Profissional', 'name': 'experiencia', 'id': 'experiencia', 'type': 'text'},
            {'label': 'Formação Acadêmica', 'name': 'formacao', 'id': 'formacao', 'type': 'text'},
            {'label': 'Contato (email/telefone)', 'name': 'contato', 'id': 'contato', 'type': 'text'},
            {'label': 'Currículo (link ou texto)', 'name': 'curriculo', 'id': 'curriculo', 'type': 'text'},
        ],
        'button_text': 'Cadastrar'
    }
    return render_template('cadastrar_desempregado.html', title="Cadastrar Desempregado", form=form)

# Função de cadastro de empresa (não alterada)
@app.route('/cadastrar_empresa', methods=['GET', 'POST'])
def cadastrar_empresa():
    if request.method == 'POST':
        nome = request.form['nome']
        vagas = request.form['vagas']
        
        # Adicionar a empresa à lista
        empresas.append({
            'nome': nome,
            'vagas': vagas
        })
        
        # Redirecionar para a área da empresa
        return redirect(url_for('area_empresa', empresa_id=nome))
    
    # Se for GET, mostrar o formulário de cadastro
    form = {
        'fields': [
            {'label': 'Nome da Empresa', 'name': 'nome', 'id': 'nome', 'type': 'text'},
            {'label': 'Descrição das Vagas', 'name': 'vagas', 'id': 'vagas', 'type': 'text'},
        ],
        'button_text': 'Cadastrar'
    }
    return render_template('cadastrar_empresa.html', title="Cadastrar Empresa", form=form)

# Outras rotas e funções continuam as mesmas...

if __name__ == '__main__':
    app.run(debug=True)
