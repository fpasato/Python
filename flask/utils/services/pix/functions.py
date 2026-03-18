from utils.validators import get_db
from uuid import uuid4

# CPF e Email fixos
def register_default_keys(conta_id, cpf, email):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO chaves_pix (conta_id, tipo, chave)
        VALUES (?, 'cpf', ?)
    """, (conta_id, cpf))

    cursor.execute("""
        INSERT OR IGNORE INTO chaves_pix (conta_id, tipo, chave)
        VALUES (?, 'email', ?)
    """, (conta_id, email))

    conn.commit()

# Recupera todas as chaves
def get_all_keys(conta_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chaves_pix WHERE conta_id = ?", (conta_id,))
    keys = cursor.fetchall()
    conn.close()
    return keys

# Gera chave aleatória única
def create_keys(conta_id):
    chave_aleatoria = str(uuid4())
    if key_exists(chave_aleatoria):
        return {"success": False, "message": "Chave já existe"}
    return {"success": True, "message": "Chave criada com sucesso", "chave": chave_aleatoria}

# Registrar chave aleatória no banco
def register_key(key, conta_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chaves_pix (conta_id, tipo, chave) VALUES (?, 'aleatoria', ?)", (conta_id, key))
    conn.commit()
    return {"success": True, "message": "Chave registrada com sucesso"}

# Deletar chave aleatória pelo ID
def delete_key_by_id(key_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chaves_pix WHERE id = ?", (key_id,))
    conn.commit()
    return {"success": True, "message": "Chave deletada com sucesso"}

# Checar se chave já existe
def key_exists(chave):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chaves_pix WHERE chave = ?", (chave,))
    key = cursor.fetchone()
    conn.close()
    return bool(key)