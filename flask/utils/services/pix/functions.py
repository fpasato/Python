from utils.validators import get_db
from uuid import uuid4

# CPF e Email fixos
def register_default_keys(conta_id, cpf, email):
    conn = get_db()
    cursor = conn.cursor()
    with conn:
        cursor.execute("""
            INSERT OR IGNORE INTO chaves_pix (conta_id, tipo, chave)
            VALUES (?, 'cpf', ?)
        """, (conta_id, cpf))

        cursor.execute("""
            INSERT OR IGNORE INTO chaves_pix (conta_id, tipo, chave)
            VALUES (?, 'email', ?)
        """, (conta_id, email))

# Recupera todas as chaves
def get_all_keys(conta_id):
    conn = get_db()
    cursor = conn.cursor()
    with conn:
        cursor.execute("SELECT * FROM chaves_pix WHERE conta_id = ?", (conta_id,))
        keys = cursor.fetchall()
    return keys


# Gera chave aleatória única
def create_random_key():
    """
    Gera uma chave aleatória única e verifica se já existe no banco de dados.
    Se já existir, gera outra chave até encontrar uma única.
    """
    chave_aleatoria = str(uuid4())
    while key_exists(chave_aleatoria):
        chave_aleatoria = str(uuid4())
        
    return {"success": True, "message": "Chave criada com sucesso", "chave": chave_aleatoria}


# Checar se chave já existe
def key_exists(chave):
    conn = get_db()
    cursor = conn.cursor()
    with conn:
        cursor.execute("SELECT * FROM chaves_pix WHERE chave = ?", (chave,))
        key = cursor.fetchone()
    return bool(key)


# Registrar chave aleatória no banco
def register_key(key, conta_id):
    conn = get_db()
    cursor = conn.cursor()
    with conn:
        cursor.execute("INSERT INTO chaves_pix (conta_id, tipo, chave) VALUES (?, 'aleatoria', ?)", (conta_id, key))
    return {"success": True, "message": "Chave registrada com sucesso"}

# Deletar chave aleatória pelo ID
def delete_key_by_id(key_id):
    conn = get_db()
    cursor = conn.cursor()
    with conn:
        cursor.execute("DELETE FROM chaves_pix WHERE id = ?", (key_id,))
    return {"success": True, "message": "Chave deletada com sucesso"}

def get_key_by_value(chave):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.id AS conta_id,
            u.nome_completo,
            u.cpf,
            cp.tipo
        FROM chaves_pix cp
        JOIN contas c ON cp.conta_id = c.id
        JOIN usuarios u ON c.usuario_id = u.id
        WHERE cp.chave = ?
    """, (chave,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "success": True,
            "data": {
                "conta_id": row[0],
                "nome": row[1],
                "cpf": row[2],
                "tipo_chave": row[3]
            }
        }
    return {"success": False}

def mask_cpf(cpf):
    return f"***.***.***-{cpf[-2:]}"
