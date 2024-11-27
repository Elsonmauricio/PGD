from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dados temporários para teste
desempregados = []
empresas = []
candidaturas = {
    'empresa_candidatos': {},  # {empresa_id: [candidato_id, ...]}
    'candidato_empresas': {}   # {candidato_id: [empresa_id, ...]}
}

@app.route('/')
def index():
    return render_template('page.html', title="Página Inicial", message="Bem-vindo ao PGD!")

@app.route('/cadastrar_desempregado', methods=['GET', 'POST'])
def cadastrar_desempregado():
    if request.method == 'POST':
        nome = request.form['nome']
        habilidades = request.form['habilidades']
        experiencia = request.form['experiencia']
        formacao = request.form['formacao']
        contato = request.form['contato']
        curriculo = request.form['curriculo']
        
        desempregados.append({
            'nome': nome,
            'habilidades': habilidades.split(', '),
            'experiencia': experiencia,
            'formacao': formacao,
            'contato': contato,
            'curriculo': curriculo
        })
        return redirect(url_for('area_desempregado', desempregado_id=nome))
    
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
    return render_template('page.html', title="Cadastrar Desempregado", form=form)

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
    return render_template('page.html', title="Cadastrar Empresa", form=form)

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
    
    # Buscar todos os candidatos disponíveis
    todos_candidatos = desempregados
    
    message = f"Bem-vindo(a) {empresa['nome']}! Você tem {len(candidatos_interessados)} candidaturas."
    
    return render_template('page.html',
                         title="Área da Empresa",
                         message=message,
                         empresa=empresa,
                         candidatos=candidatos_interessados,
                         todos_candidatos=todos_candidatos)

@app.route('/pesquisar_candidatos', methods=['POST'])
def pesquisar_candidatos():
    habilidade_busca = request.form.get('habilidade', '').lower()
    empresa_id = request.form.get('empresa_id')
    
    # Encontrar a empresa
    empresa = next((e for e in empresas if e['nome'] == empresa_id), None)
    if not empresa:
        return redirect(url_for('index'))
    
    # Filtrar candidatos
    candidatos_filtrados = [
        d for d in desempregados 
        if any(habilidade_busca in h.lower() for h in d['habilidades'])
    ]
    
    # Buscar candidaturas para esta empresa
    candidaturas_empresa = candidaturas.get(empresa_id, [])
    
    return render_template('page.html',
                         title="Resultado da Pesquisa",
                         message="Resultados da pesquisa por habilidade",
                         empresa=empresa,
                         candidatos=candidatos_filtrados,
                         todos_candidatos=desempregados)

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
    
    return render_template('page.html',
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

@app.route('/pesquisar_empresas', methods=['POST'])
def pesquisar_empresas():
    vaga_busca = request.form.get('vaga', '').lower()
    desempregado_id = request.form.get('desempregado_id')
    
    # Encontrar o desempregado
    desempregado = next((d for d in desempregados if d['nome'] == desempregado_id), None)
    
    # Filtrar empresas
    empresas_filtradas = [
        e for e in empresas 
        if vaga_busca in e['vagas'].lower()
    ]
    
    # Buscar candidaturas do desempregado
    minhas_candidaturas = [
        empresa['nome'] for empresa in empresas 
        if desempregado_id in candidaturas.get(empresa['nome'], [])
    ]
    
    return render_template('page.html',
                         title="Resultado da Pesquisa",
                         desempregado=desempregado,
                         empresas=empresas_filtradas,
                         minhas_candidaturas=minhas_candidaturas)

# @app.route('/listar_desempregados')
# def listar_desempregados():
#     items = [f"{d['nome']} - Habilidades: {', '.join(d['habilidades'])}" for d in desempregados]
#     return render_template('page.html', title="Lista de Desempregados", items=items)

# @app.route('/listar_empresas')
# def listar_empresas():
#     items = [f"{e['nome']} - Vagas: {e['vagas']}" for e in empresas]
#     return render_template('page.html', title="Lista de Empresas", items=items)

if __name__ == '__main__':
    app.run(debug=True)
