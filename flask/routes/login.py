from flask import Blueprint, session, redirect, render_template, request
import re
from utils.validators import get_db
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__, url_prefix="/login")

@login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        cursor = conn.cursor()  
        email = request.form.get("email") 
        password = request.form.get("password")

        cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))        
        account = cursor.fetchone()
        
        if not account:
            return render_template("login/index.html", popup_message="Email não encontrado", popup_type="error")
        
        if not check_password_hash(account[4], password):
            return render_template("login/index.html", popup_message="Senha incorreta", popup_type="error")
        
        # SUCESSO: Salva os dados na sessão
        user_info = {
            'user_id': account[0],
            'user_name': account[1].split()[0],
            'cpf': account[2],
            'email': account[3],
            'senha': account[4]
        }
        session['user_info'] = user_info
        
        # Obter número da conta do usuário
        cursor.execute("SELECT numero_conta FROM contas WHERE usuario_id = ?", (account[0],))
        conta_result = cursor.fetchone()
        if conta_result:
            session['numero_conta'] = conta_result[0]
        return redirect("/home")
    
    return render_template("login/index.html")