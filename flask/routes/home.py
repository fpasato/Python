from flask import Blueprint, session, redirect, render_template
from utils.validators import check_session

home_bp = Blueprint("home", __name__, url_prefix="/home")

@home_bp.route("/")
def home():
    if not check_session():
        return redirect("/login")
    
    return render_template("home/index.html", nome_usuario=session['user_info']['user_name'])