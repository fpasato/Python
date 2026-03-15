from flask import Flask, redirect, session

from routes.home import home_bp
from routes.login import login_bp  
from routes.register import register_bp
from routes.transfer import transfer_bp

app = Flask(__name__)
app.secret_key = "segredo_super_secreto"

# Registra todos os blueprints
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(transfer_bp)



@app.route("/")
def index():
    return redirect("/login")

        
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)