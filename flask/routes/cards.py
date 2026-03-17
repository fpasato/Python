
from flask import Blueprint, render_template, session
from utils.services.cards.functions import create_card
from utils.validators import get_db

cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

@cards_bp.route("/")
def cards():

    create_card()
    
    
    
    
    return render_template("cards/index.html")
