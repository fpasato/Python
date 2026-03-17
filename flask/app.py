from flask import Flask, redirect, session

from routes.home import home_bp
from routes.login import login_bp  
from routes.register import register_bp
from routes.transfer import transfer_bp
from routes.versaldo import versaldo_bp
from routes.emprestimos import emprestimos_bp
from routes.pix import pix_bp
from routes.cards import cards_bp

app = Flask(__name__)
app.secret_key = "segredo_super_secreto"

# Registra todos os blueprints
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(transfer_bp)
app.register_blueprint(versaldo_bp)
app.register_blueprint(emprestimos_bp)
app.register_blueprint(pix_bp)
app.register_blueprint(cards_bp)


@app.route("/")
def index():
    return redirect("/login")

        
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)