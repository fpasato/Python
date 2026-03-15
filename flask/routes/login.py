from flask import Blueprint, session, redirect, render_template, request
import re
import hashlib
from utils.validators import get_db

login_bp = Blueprint("login", __name__, url_prefix="/login")

@login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db()
        cursor = conn.cursor()  
        cpf = re.sub(r"\D", "", request.form.get("cpf")) 
        password = request.form.get("password")

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM contas WHERE cpf = ?", (cpf,))        
        account = cursor.fetchone()
        
        if not account:
            return render_template("login/index.html", popup_message="CPF não encontrado", popup_type="error")
        
        if account[3] != password_hash:
            return render_template("login/index.html", popup_message="Senha incorreta", popup_type="error")
        
        # SUCESSO: Salva os dados na sessão
        session['user_id'] = account[0]
        session['user_name'] = account[1].split()[0]     
        return redirect("/home")
    return render_template("login/index.html")