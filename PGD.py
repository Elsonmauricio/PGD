from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dados temporários para teste
desempregados = []
empresas = []
candidaturas = {
    'empresa_candidatos': {},  # {empresa_id: [candidato_id, ...]}
    'candidato_empresas': {}   # {candidato_id: [empresa_id, ...]}
}

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html', title="Página Inicial", message="Bem-vindo ao PGD!")

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
        return redirect(url_for('index'))  # Redireciona para a página inicial após o cadastro

    # Renderiza o formulário
    form = {
        'fields': [
            {'label': 'Nome', 'name': 'nome', 'id': 'nome', 'type': 'text'},
            {'label': 'Habilidades (separadas por vírgula)', 'name': 'habilidades', 'id': 'habilidades', 'type': 'text'},
            {'label': 'Experiência Profissional', 'name': 'experiencia', 'id': 'experiencia', 'type': 'textarea'},
            {'label': 'Formação Acadêmica', 'name': 'formacao', 'id': 'formacao', 'type': 'text'},
            {'label': 'Contato (email/telefone)', 'name': 'contato', 'id': 'contato', 'type': 'text'},
            {'label': 'Currículo (link ou texto)', 'name': 'curriculo', 'id': 'curriculo', 'type': 'textarea'},
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
            {'label': 'Descrição das Vagas', 'name': 'vagas', 'id': 'vagas', 'type': 'textarea'},
        ],
        'button_text': 'Cadastrar'
    }
    return render_template('cadastrar_empresa.html', title="Cadastrar Empresa", form=form)

@app.route('/area_empresa/<empresa_id>')
def area_empresa(empresa_id):
    # Encontrar a empresa pelo ID
    empresa = next((e for e in empresas if e['nome'] == empresa_id), None)
    if not empresa:
        return redirect(url_for('index'))
    
    # Buscar candidaturas para esta empresa
    candidatos_ids = candidaturas['empresa_candidatos'].get(empresa_id, [])
    candidatos_interessados = [
        d for d in desempregados 
        if d['nome'] in candidatos_ids
    ]
    
    # Mensagem para a área da empresa
    message = f"Bem-vindo(a) {empresa['nome']}! Você tem {len(candidatos_interessados)} candidaturas."
    
    return render_template('area_empresa_candidato.html',
                           empresa=empresa,
                           message=message,
                           candidatos=candidatos_interessados,
                           desempregado=None,  # Se não houver um desempregado logado, pode ser None
                           minhas_candidaturas=candidaturas['empresa_candidatos'].get(empresa_id, []))

@app.route('/area_desempregado/<desempregado_id>')
def area_desempregado(desempregado_id):
    # Encontrar o desempregado pelo ID
    desempregado = next((d for d in desempregados if d['nome'] == desempregado_id), None)
    if not desempregado:
        return redirect(url_for('index'))
    
    # Buscar todas as empresas disponíveis
    empresas_disponiveis = empresas
    # Buscar candidaturas deste desempregado
    minhas_candidaturas = candidaturas['candidato_empresas'].get(desempregado_id, [])
    
    message = f"Bem-vindo(a) {desempregado['nome']}! Você tem {len(minhas_candidaturas)} candidaturas enviadas."
    
    return render_template('indexe.html',
                         title="Área do Candidato",
                         message=message,
                         desempregado=desempregado,
                         empresas=empresas_disponiveis,
                         minhas_candidaturas=minhas_candidaturas)

@app.route('/enviar_candidatura', methods=['POST'])
def enviar_candidatura():
    empresa_id = request.form.get('empresa_id')
    candidato_id = request.form.get('candidato_id')
    
    # Registrar candidatura para a empresa
    if empresa_id not in candidaturas['empresa_candidatos']:
        candidaturas['empresa_candidatos'][empresa_id] = []
    if candidato_id not in candidaturas['empresa_candidatos'][empresa_id]:
        candidaturas['empresa_candidatos'][empresa_id].append(candidato_id)
    
    # Registrar candidatura para o candidato
    if candidato_id not in candidaturas['candidato_empresas']:
        candidaturas['candidato_empresas'][candidato_id] = []
    if empresa_id not in candidaturas['candidato_empresas'][candidato_id]:
        candidaturas['candidato_empresas'][candidato_id].append(empresa_id)
    
    return redirect(url_for('area_desempregado', desempregado_id=candidato_id))


@app.route('/area_empresa_candidato/<empresa_id>/<desempregado_id>')
def area_empresa_candidato(empresa_id, desempregado_id):
    # Encontrar a empresa pelo ID
    empresa = next((e for e in empresas if e['nome'] == empresa_id), None)
    if not empresa:
        return redirect(url_for('index'))
    
    # Encontrar o desempregado pelo ID
    desempregado = next((d for d in desempregados if d['nome'] == desempregado_id), None)
    if not desempregado:
        return redirect(url_for('index'))
    
    # Buscar candidaturas para esta empresa
    candidatos_ids = candidaturas['empresa_candidatos'].get(empresa_id, [])
    candidatos_interessados = [
        d for d in desempregados 
        if d['nome'] in candidatos_ids
    ]
    
    # Buscar todos os candidatos disponíveis
    todos_candidatos = desempregados
    
    # Mensagens para ambas as áreas
    message_empresa = f"Bem-vindo(a) {empresa['nome']}! Você tem {len(candidatos_interessados)} candidaturas."
    message_candidato = f"Bem-vindo(a) {desempregado['nome']}! Você tem {len(candidaturas['candidato_empresas'].get(desempregado_id, []))} candidaturas enviadas."
    
    return render_template('area_empresa_candidato.html',
                           empresa=empresa,
                           candidatos=candidatos_interessados,
                           todos_candidatos=todos_candidatos,
                           desempregado=desempregado,
                           minhas_candidaturas=candidaturas['candidato_empresas'].get(desempregado_id, []),
                           message=message_empresa,
                           message_candidato=message_candidato)
if __name__ == '__main__':
    app.run(debug=True)
