from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dados temporários para teste
desempregados = []
empresas = []

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('page.html', title="Página Inicial", message="Bem-vindo ao PGD!")

# Rota para a página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Lógica de validação do login (pode ser implementada conforme necessário)
        # Se o login for bem-sucedido, você pode redirecionar o usuário para outra página
        # Exemplo: return redirect(url_for('index'))
        
        return redirect(url_for('index'))  # Redirecionando para a página inicial após o login

    # Se o método for GET (ou seja, a página é acessada inicialmente), renderize o HTML do login
    return render_template('login.html', title="Login")

# Função de cadastro de desempregado (não alterada)
@app.route('/cadastrar_desempregado', methods=['GET', 'POST'])
def cadastrar_desempregado():
    if request.method == 'POST':
        nome = request.form['nome']
        habilidades = request.form['habilidades']
        desempregados.append({'nome': nome, 'habilidades': habilidades.split(', ')})
        return redirect(url_for('listar_desempregados'))
    form = {
        'fields': [
            {'label': 'Nome', 'name': 'nome', 'id': 'nome', 'type': 'text'},
            {'label': 'Habilidades (separadas por vírgula)', 'name': 'habilidades', 'id': 'habilidades', 'type': 'text'},
        ],
        'button_text': 'Cadastrar'
    }
    return render_template('page.html', title="Cadastrar Desempregado", form=form)

# Função de cadastro de empresa (não alterada)
@app.route('/cadastrar_empresa', methods=['GET', 'POST'])
def cadastrar_empresa():
    if request.method == 'POST':
        nome = request.form['nome']
        vagas = request.form['vagas']
        empresas.append({'nome': nome, 'vagas': vagas})
        return redirect(url_for('listar_empresas'))
    form = {
        'fields': [
            {'label': 'Nome da Empresa', 'name': 'nome', 'id': 'nome', 'type': 'text'},
            {'label': 'Descrição das Vagas', 'name': 'vagas', 'id': 'vagas', 'type': 'text'},
        ],
        'button_text': 'Cadastrar'
    }
    return render_template('page.html', title="Cadastrar Empresa", form=form)

if __name__ == '__main__':
    app.run(debug=True)
