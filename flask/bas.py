import sqlite3

# conecta ao banco (cria se não existir)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# cria a tabela contas
cursor.execute("""
CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT NOT NULL,
    cpf TEXT NOT NULL,
    senha TEXT NOT NULL,
    saldo REAL DEFAULT 0,
    extrato TEXT,
    numero_conta TEXT
)
""")

conn.commit()
conn.close()

print("Tabela 'contas' criada com sucesso!")