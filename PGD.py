from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dados temporários para teste
desempregados = []
empresas = []

@app.route('/')
def index():
    return render_template('page.html', title="Página Inicial", message="Bem-vindo ao PGD!")

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

@app.route('/listar_desempregados')
def listar_desempregados():
    items = [f"{d['nome']} - Habilidades: {', '.join(d['habilidades'])}" for d in desempregados]
    return render_template('page.html', title="Lista de Desempregados", items=items)

@app.route('/listar_empresas')
def listar_empresas():
    items = [f"{e['nome']} - Vagas: {e['vagas']}" for e in empresas]
    return render_template('page.html', title="Lista de Empresas", items=items)

if __name__ == '__main__':
    app.run(debug=True)
