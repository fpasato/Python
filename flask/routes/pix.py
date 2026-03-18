from flask import Blueprint, render_template, session, redirect, request, jsonify
from utils.validators import get_db
from utils.services.pix.functions import (
    get_all_keys, create_keys, register_key, delete_key_by_id, register_default_keys
)

pix_bp = Blueprint("pix", __name__, url_prefix="/pix")

@pix_bp.route("/", methods=["GET"])
def pix():
    numero_conta = session.get('numero_conta')
    if not numero_conta:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contas WHERE numero_conta = ?", (numero_conta,))
    conta = cursor.fetchone()
    db.close()

    if not conta:
        return redirect("/login")

    conta_id = conta[0]
    
    # CPF e email sempre registrados se não existirem
    cpf = session['user_info']['cpf']
    email = session['user_info']['email']
    register_default_keys(conta_id, cpf, email)

    keys = get_all_keys(conta_id)

    # Campo de chave aleatória sempre vazio no início
    return render_template("pix/index.html", conta=conta, keys=keys, chave_aleatoria="")

# Registrar chave aleatória gerada
@pix_bp.route("/registrar-chave", methods=["POST"])
def registrar_chave():
    data = request.get_json()
    chave = data.get("chave")
    if not chave:
        return jsonify({"success": False, "message": "Nenhuma chave gerada para registrar"})

    numero_conta = session.get('numero_conta')
    if not numero_conta:
        return jsonify({"success": False, "message": "Usuário não logado"})

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contas WHERE numero_conta = ?", (numero_conta,))
    conta = cursor.fetchone()
    db.close()
    
    if not conta:
        return jsonify({"success": False, "message": "Conta não encontrada"})

    conta_id = conta[0]
    result = register_key(chave, conta_id)
    return jsonify(result)

# Gerar chave aleatória
@pix_bp.route("/gerar-chave", methods=["POST"])
def gerar_chave():
    numero_conta = session.get('numero_conta')
    if not numero_conta:
        return jsonify({"success": False, "message": "Usuário não logado"})
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contas WHERE numero_conta = ?", (numero_conta,))
    conta = cursor.fetchone()
    db.close()
    
    if not conta:
        return jsonify({"success": False, "message": "Conta não encontrada"})
    
    conta_id = conta[0]
    result = create_keys(conta_id)
    return jsonify(result)

# Excluir chave aleatória (não pode excluir cpf/email)
@pix_bp.route("/excluir-chave/<int:key_id>", methods=["POST"])
def excluir_chave(key_id):
    # Verifica se a chave existe e se não é cpf/email
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo FROM chaves_pix WHERE id = ?", (key_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"success": False, "message": "Chave não encontrada"})

    if row[0] in ["cpf", "email"]:
        return jsonify({"success": False, "message": "Não é possível excluir CPF ou Email"})

    result = delete_key_by_id(key_id)
    return jsonify(result)