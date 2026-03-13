import json
import os

# Sessão global para armazenar usuário logado
usuario_logado = None

def set_usuario_logado(usuario):
    """Define o usuário logado na sessão"""
    global usuario_logado
    usuario_logado = usuario

def get_usuario_logado():
    """Retorna o usuário logado na sessão"""
    global usuario_logado
    return usuario_logado

def logout():
    """Remove o usuário da sessão"""
    global usuario_logado
    usuario_logado = None

def salvar_dados():
    """Salva os dados atualizados no arquivo JSON"""
    caminho_json = os.path.join(os.path.dirname(os.path.dirname(__file__)), "contas.json")
    
    # Ler dados atuais
    with open(caminho_json, "r") as f:
        dados = json.load(f)
    
    # Atualizar dados do usuário logado
    cpf_usuario = usuario_logado.get('cpf') if usuario_logado else None
    if cpf_usuario and cpf_usuario in dados:
        dados[cpf_usuario] = usuario_logado
    
    # Salvar dados atualizados
    with open(caminho_json, "w") as f:
        json.dump(dados, f, indent=2)