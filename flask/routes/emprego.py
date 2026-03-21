
from flask import Blueprint, render_template

emprego_bp = Blueprint("escolher-emprego", __name__, url_prefix="/escolher-emprego")

@emprego_bp.route("/")
def escolher_emprego():
    
    return render_template("empregos/index.html")   
