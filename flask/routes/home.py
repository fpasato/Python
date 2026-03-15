from flask import Blueprint, session, redirect, render_template

home_bp = Blueprint("home", __name__, url_prefix="/home")

@home_bp.route("/")
def home():
    if 'user_id' not in session:
        return redirect("/login")
    return render_template("home/index.html", nome_usuario=session['user_name'])