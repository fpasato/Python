import hashlib
import re
from utils.validators import get_db, cpf_exists, account_already_exists, verifica_cpf

import time
import random

def gerar_numero_conta():
    tempo = int(time.time())
    aleatorio = random.randint(100,999)

    numero = str(tempo)[-5:] + str(aleatorio)
    return numero


def register_account(form_data):
    """
    Recebe form_data do Flask (request.form) e tenta criar a conta.
    Retorna dict: {"success": bool, "message": str, "numero_conta": str (opcional)}
    """
    nome = form_data.get("name")
    cpf = re.sub(r"\D", "", form_data.get("cpf"))
    senha = form_data.get("password")
    confirmar_senha = form_data.get("confirm_password")

    # valida senha
    if senha != confirmar_senha:
        return {"success": False, "message": "As senhas não conferem"}

    # valida CPF
    if not verifica_cpf(cpf):
        return {"success": False, "message": "CPF inválido"}

    # verifica CPF duplicado
    if cpf_exists(cpf):
        return {"success": False, "message": "CPF já cadastrado"}

    # gera número de conta único
    numero_conta = gerar_numero_conta()
    while account_already_exists(numero_conta):
        numero_conta = gerar_numero_conta()

    # criptografa senha
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    # insere no banco
    conn = get_db()
    cursor = conn.cursor()
    with conn:
        cursor.execute(
            "INSERT INTO contas (nome_completo, cpf, senha, saldo, numero_conta) VALUES (?, ?, ?, ?, ?)",
            (nome, cpf, senha_hash, 150000, numero_conta)
        )

    return {"success": True, "message": "Conta criada! Faça seu login.", "numero_conta": numero_conta}