
import os
import sqlite3

# Caminho absoluto do banco, garante que sempre vai abrir o correto
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
    

def account_already_exists(numero_conta):
    conn = get_db()
    cursor = conn.cursor()
    
    with conn:
        cursor.execute("SELECT 1 FROM contas WHERE numero_conta=? LIMIT 1", (numero_conta,))
        resultado = cursor.fetchone()
    
    return resultado is not None

def cpf_exists(cpf):
    conn = get_db()
    cursor = conn.cursor()
    
    with conn:
        cursor.execute("SELECT 1 FROM contas WHERE cpf=? LIMIT 1", (cpf,))
        resultado = cursor.fetchone()
    
    return resultado is not None


def verifica_cpf(cpf):
    
    if len(cpf) != 11:
        return False
    
    # verifica d1
    soma, indice_digito = 0, 0
    for n in range(10, 1, -1): 
        soma += int(cpf[indice_digito]) * n
        indice_digito +=1
    d1 = 0 if soma % 11 < 2 else 11 - (soma % 11)

    # verifica d2
    soma, indice_digito = 0, 0
    for n in range(11, 2, -1):
        soma += int(cpf[indice_digito]) * n
        indice_digito +=1
    soma += d1 * 2
    
    d2 = 0 if soma % 11 < 2 else 11- (soma % 11)

    if d1 == int(cpf[-2]) and d2 == int(cpf[-1]):
        return True
    else:
        return False
    






def get_account_by_number(numero_conta):
    conn = get_db()
    cursor = conn.cursor()
    
    with conn:
        cursor.execute("SELECT * FROM contas WHERE numero_conta=?", (numero_conta,))
        resultado = cursor.fetchone()
    
    if resultado is None:
        return False
    
    # Se encontrou, retorna os dados da conta
    conta = {
        'nome_completo': resultado[1],
        'numero_conta': resultado[6]
    }
    
    return conta 


def get_account_by_id(id):
    conn = get_db()
    cursor = conn.cursor()
    
    with conn:
        cursor.execute("SELECT * FROM contas WHERE id=?", (id,))
        resultado = cursor.fetchone()
    
    if resultado is None:
        return False
    
    # Se encontrou, retorna os dados da conta
    conta = {
        'id': resultado[0], 
        'nome_completo': resultado[1],
        'cpf': resultado[2],
        'saldo': resultado[4],
        'numero_conta': resultado[6]
    }
    
    return conta 