from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from banco import verifica_cliente

app = Flask(__name__)
app.secret_key = 'banco_liso_secret_key'

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    cpf = request.form.get('cpf', '').strip()
    
    if not cpf:
        flash('CPF não pode estar vazio!', 'error')
        return redirect(url_for('index'))
    
    if verifica_cliente(cpf):
        session['cpf'] = cpf
        caminho_json = os.path.join(os.path.dirname(__file__), 'contas.json')
        with open(caminho_json) as f:
            clientes = json.load(f)
        session['cliente'] = clientes[cpf]
        return redirect(url_for('dashboard'))
    else:
        flash('Cliente não encontrado!', 'error')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'cpf' not in session:
        return redirect(url_for('index'))
    cliente = session.get('cliente', {})
    return render_template('dashboard.html', cliente=cliente)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)