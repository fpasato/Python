import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# ativa foreign key
conn.execute("PRAGMA foreign_keys = ON")

# 👤 USUARIOS (login)
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# 💰 CONTAS (dinheiro)
cursor.execute("""
CREATE TABLE IF NOT EXISTS contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    numero_conta TEXT NOT NULL UNIQUE,
    saldo REAL DEFAULT 0,

    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)
""")

# 📄 TRANSACOES (extrato)
cursor.execute("""
CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conta_id INTEGER NOT NULL,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL,
    descricao TEXT,
    data DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conta_id) REFERENCES contas(id)
)
""")

# 💳 CARTOES
cursor.execute("""
CREATE TABLE IF NOT EXISTS cartoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conta_id INTEGER NOT NULL,
    numero_cartao TEXT NOT NULL UNIQUE,
    validade TEXT,
    cvv TEXT,
    limite REAL,
    tipo TEXT,

    FOREIGN KEY (conta_id) REFERENCES contas(id)
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso 🚀")