from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuração do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Use SQLite como banco de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Inicializa o SQLAlchemy

# Definindo a chave secreta para sessões
app.secret_key = 'sua_chave_secreta_aqui'

# Modelo para a Tabela de Usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Rota para a página inicial (restrita a usuários logados)
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redireciona para o login se não estiver logado
    
    # Exibe a página inicial com o nome do usuário logado
    return render_template('index.html', title="Página Inicial", message=f"Bem-vindo, {session['user_name']}!")

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Verifica se o email existe na base de dados
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password, password):
            # Se as credenciais forem corretas, armazena as informações na sessão
            session['user_id'] = usuario.id  # Armazena o ID do usuário
            session['user_name'] = usuario.name  # Armazena o nome do usuário

            # Redireciona para a página inicial após o login bem-sucedido
            return redirect(url_for('index'))

        else:
            # Se não encontrar o usuário ou a senha estiver incorreta
            return render_template('login.html', title="Login", error="Email ou senha inválidos")
    
    # Exibe o formulário de login para o método GET
    return render_template('login.html', title="Login")

# Rota para registro de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['signup_email']
        password = request.form['signup_password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('register.html', title="Register", error="Passwords do not match.")
        
        hashed_password = generate_password_hash(password)
        novo_usuario = Usuario(name=name, email=email, password=hashed_password)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html', title="Register")

# Rota para cadastrar desempregado
@app.route('/cadastrar_desempregado', methods=['GET', 'POST'])
def cadastrar_desempregado():
    if request.method == 'POST':
        nome = request.form['nome']
        habilidades = request.form['habilidades']
        experiencia = request.form['experiencia']
        formacao = request.form['formacao']
        contato = request.form['contato']
        curriculo = request.form['curriculo']
        
        # Salve os dados do desempregado no banco (modelo necessário)
        return redirect(url_for('index'))

    return render_template('cadastrar_desempregado.html', title="Cadastrar Desempregado")

# Rota para cadastrar empresa
@app.route('/cadastrar_empresa', methods=['GET', 'POST'])
def cadastrar_empresa():
    if request.method == 'POST':
        nome = request.form['nome']
        vagas = request.form['vagas']
        
        # Salve os dados da empresa no banco (modelo necessário)
        return redirect(url_for('index'))

    return render_template('cadastrar_empresa.html', title="Cadastrar Empresa")

# Logout
@app.route('/logout')
def logout():
    session.clear()  # Remove todos os dados da sessão
    return redirect(url_for('login'))  # Redireciona para a página de login

# Inicializando o Banco de Dados
@app.before_request
def init_db():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
