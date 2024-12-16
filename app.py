import sqlite3

# Conexão com o banco de dados SQLite (ou cria o arquivo se não existir)
conn = sqlite3.connect('database.sqlite')

# Criar um cursor para executar comandos SQL
cursor = conn.cursor()

# Criar a tabela de login
cursor.execute('''
    CREATE TABLE IF NOT EXISTS login (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Criar a tabela de criar_conta
cursor.execute('''
    CREATE TABLE IF NOT EXISTS criar_conta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        signup_email TEXT NOT NULL UNIQUE,
        signup_password TEXT NOT NULL,
        confirm_password TEXT NOT NULL
    )
''')

# Criar também as tabelas já existentes para desempregados e empresas, conforme você já tinha
# Tabela de desempregados
cursor.execute('''
    CREATE TABLE IF NOT EXISTS desempregados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        habilidades TEXT,
        experiencia TEXT,
        formacao TEXT,
        contato TEXT,
        curriculo TEXT
    )
''')

# Tabela de empresas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS empresas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        vagas TEXT
    )
''')

# Tabela para registrar candidaturas (empresa_candidatos)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS empresa_candidatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empresa_id INTEGER NOT NULL,
        candidato_id INTEGER NOT NULL,
        FOREIGN KEY(empresa_id) REFERENCES empresas(id),
        FOREIGN KEY(candidato_id) REFERENCES desempregados(id)
    )
''')

# Tabela para registrar candidaturas de candidatos (candidato_empresas)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidato_empresas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidato_id INTEGER NOT NULL,
        empresa_id INTEGER NOT NULL,
        FOREIGN KEY(candidato_id) REFERENCES desempregados(id),
        FOREIGN KEY(empresa_id) REFERENCES empresas(id)
    )
''')

# Confirmar as alterações e fechar a conexão
conn.commit()
conn.close()
