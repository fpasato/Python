from sqlite3 import Date
from utils.validators import get_db
import random
import time

def create_card():
    conta_id = get_conta_id()
        
    # data_validade a 5 anos
    validade = time.strftime("%m/%y", time.localtime(time.time() + 5 * 365 * 24 * 60 * 60))
    cvv = f"{random.randint(0, 999):03d}"
    numero_cartao = gera_numero_cartao()
    tipo = "credito"
    limite = 1000.00
    
    # Verifica se o cartão já existe
    while check_card(numero_cartao):
        numero_cartao = gera_numero_cartao()

    conn = get_db()
    cursor = conn.cursor()
    
    with conn:
        cursor.execute("INSERT INTO cartoes (conta_id, numero_cartao,validade,cvv,limite, tipo) VALUES (?, ?, ?, ?, ?, ?)", (conta_id, numero_cartao, validade, cvv, limite, tipo))
    return {"success": True, "message": "Cartão criado com sucesso"}



def get_conta_id():
    user_id = session.get('user_info', {}).get('user_id')
    
    if user_id:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM contas WHERE usuario_id = ?", (user_id,))
        result = cursor.fetchone()
        if not result:
            return {"success": False, "message": "Conta não encontrada"}
        
        id_conta = result[0]
    
    return id_conta
    

def check_card(numero_cartao):
    conn = get_db()
    cursor = conn.cursor()

    with conn:
        cursor.execute("SELECT * FROM cartoes WHERE numero_cartao = ?", (numero_cartao,))
    
    result = cursor.fetchall()
    
    # se cartão existir, retorna True
    if result:
        return True
    return False

    

def get_card():
    pass


def delete_card():
    pass


# Gera número de cartão com 11 dígitos
def gera_numero_cartao():
    numero = ''.join([str(random.randint(0, 9)) for _ in range(11)])
    return numero