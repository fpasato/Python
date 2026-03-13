import json

from services.banco import verifica_cliente
import os

def login(cpf, senha):
    caminho_json = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contas.json")
    with open(caminho_json) as f:
        contas = json.load(f)
        
    if verifica_cliente(cpf):
        if contas[cpf].get("senha") == senha:
            return contas[cpf]
    return None

