

from flask import Blueprint, render_template

pix_bp = Blueprint("pix", __name__, url_prefix="/pix")

@pix_bp.route("/")
def pix():
    return render_template("pix/index.html")
