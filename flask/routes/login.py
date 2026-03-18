from flask import Blueprint, session, redirect, render_template, request
import re
from utils.validators import get_db
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__, url_prefix="/login")
@login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return render_template(
                "login/index.html",
                popup_message="Preencha todos os campos",
                popup_type="error"
            )

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT id, nome_completo, cpf, email, senha 
                FROM usuarios 
                WHERE email = ?
            """, (email,))
            
            account = cursor.fetchone()

            if not account:
                return render_template(
                    "login/index.html",
                    popup_message="Email não encontrado",
                    popup_type="error"
                )

            if not check_password_hash(account[4], password):
                return render_template(
                    "login/index.html",
                    popup_message="Senha incorreta",
                    popup_type="error"
                )

            # Conta
            cursor.execute(
                "SELECT numero_conta, saldo FROM contas WHERE usuario_id = ?",
                (account[0],)
            )
            conta_result = cursor.fetchone()

        finally:
            conn.close()

        # Session
        session['user_info'] = {
            'user_id': account[0],
            'user_name': account[1].split()[0],
            'user_full_name': account[1],
            'cpf': account[2],
            'email': account[3],
            'conta_numero': conta_result[0] if conta_result else None
        }
        
        # Salva número da conta na sessão
        if conta_result:
            session['numero_conta'] = conta_result[0]

        return redirect("/home")

    return render_template("login/index.html")