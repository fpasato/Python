from flask import Flask, redirect, session
from utils.auto import start_scheduler
import os

from routes.home import home_bp
from routes.login import login_bp  
from routes.register import register_bp
from routes.transfer import transfer_bp
from routes.versaldo import versaldo_bp
from routes.emprestimos import emprestimos_bp
from routes.pix import pix_bp
from routes.cards import cards_bp
from routes.investimento import investimento_bp
from routes.emprego import emprego_bp
from routes.faturas import faturas_bp  
from routes.extrato import extrato_bp




app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_key")

# Registra todos os blueprints
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(transfer_bp)
app.register_blueprint(versaldo_bp)
app.register_blueprint(emprestimos_bp)
app.register_blueprint(pix_bp)
app.register_blueprint(cards_bp)
app.register_blueprint(investimento_bp)
app.register_blueprint(emprego_bp)
app.register_blueprint(faturas_bp)
app.register_blueprint(extrato_bp)


@app.route("/")
def index():
    return redirect("/login")

        
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")



if not getattr(app, "_scheduler_started", False):
    start_scheduler()
    app._scheduler_started = True

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)