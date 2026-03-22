
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from utils.validators import check_session, get_db
from utils.services.banco.faturas import get_faturas, pagar_fatura, registrar_transacao, deletar_fatura, get_valor_fatura

faturas_bp = Blueprint("faturas", __name__, url_prefix="/faturas")

@faturas_bp.route('/')
def index():
    if not check_session():
        return redirect(url_for('login.login'))
    
    conta_id = session['user_info']['conta_id']
    faturas = get_faturas(conta_id)
    return render_template('faturas/index.html', faturas=faturas)



@faturas_bp.route('/pagar', methods=['POST'])
def processar_pagamento():
    if not check_session():
        return redirect(url_for('login.login'))
    
    """
    Processa o pagamento de uma fatura:
    1. Valida se a fatura existe e pertence ao usuário
    2. Verifica se há saldo suficiente
    3. Debita o valor da conta
    4. Registra a transação
    5. Remove a fatura do sistema
    """
    
    fatura_id = request.form.get('fatura_id')
    conta_id = session['user_info']['conta_id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    fatura = get_valor_fatura(fatura_id, conta_id)
    
    if not fatura:
        conn.close()
        return jsonify({"error": "Fatura não encontrada"}), 404
    
    valor_fatura = fatura[0]
    
    # Buscar saldo da conta
    cursor.execute("SELECT saldo FROM contas WHERE id = ?", (conta_id,))
    saldo_result = cursor.fetchone()
    
    # Verificar se tem saldo suficiente
    if not saldo_result or saldo_result[0] < valor_fatura:
        conn.close()
        return jsonify({"error": "Saldo insuficiente"}), 400
    
    # Atualizar saldo
    novo_saldo = saldo_result[0] - valor_fatura
    cursor.execute("UPDATE contas SET saldo = ? WHERE id = ?", (novo_saldo, conta_id))
    
    # Marcar fatura como paga
    cursor.execute("UPDATE faturas SET status = 'pago' WHERE id = ?", (fatura_id,))
    
    # Registrar transação
    cursor.execute("""
        INSERT INTO transacoes_conta (conta_id, valor, tipo, descricao)
        VALUES (?, ?, 'debito', 'Pagamento de fatura')
    """, (conta_id, valor_fatura))
    
    # Deletar fatura
    cursor.execute("DELETE FROM faturas WHERE id = ?", (fatura_id,))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('faturas.index'))    
