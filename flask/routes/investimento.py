
import sqlite3
from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from utils.services.banco.investimento import (
    carregar_carteira ,load_all_investiments, sell_investment, history_prices, buy_investment
)
from utils.validators import get_db

investimento_bp = Blueprint('investimento', __name__)

@investimento_bp.route("/investimento")
def investimento():
    if 'user_info' not in session:
        return redirect(url_for('auth.login'))

    conta_id = session['user_info']['conta_id']

    # Recupera mensagem de popup da sessão e limpa
    popup_message = session.pop('popup_message', None)
    popup_type = session.pop('popup_type', None)

    investimentos_data = load_all_investiments()
    investimentos_disponiveis = investimentos_data['investimentos']

    carteira_data = carregar_carteira(conta_id)
    conn = get_db()
    conn.row_factory = sqlite3.Row
    conta = conn.execute("SELECT saldo FROM contas WHERE id = ?", (conta_id,)).fetchone()
    saldo_atual = conta['saldo'] if conta else 0
    conn.close()

    if not carteira_data or not carteira_data.get('investimentos'):
        carteira = []
        valor_carteira = 0
    else:
        carteira = carteira_data['investimentos']
        valor_carteira = sum(item['saldo'] for item in carteira) if carteira else 0

    return render_template(
        "investimento/index.html",
        carteira=carteira,
        investimentos_disponiveis=investimentos_disponiveis,
        valor_carteira=valor_carteira,
        saldo=saldo_atual,
        session=session,
        popup_message=popup_message,
        popup_type=popup_type
    )
   
    
    
@investimento_bp.route("/investimento/historico/<int:investimento_id>")
def historico(investimento_id):
    """API para retornar histórico de preços."""
    try:
        history = history_prices(investimento_id)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@investimento_bp.route("/investimento/comprar", methods=["POST"])
def comprar():
    if 'user_info' not in session:
        return redirect(url_for('auth.login'))

    conta_id = session['user_info']['conta_id']
    investimento_id = request.form.get('investimento_id')
    quantidade = int(request.form.get('quantidade', 1))
    tempo = request.form.get('tempo')

    success = buy_investment(conta_id, investimento_id, quantidade, tempo)

    if success:
        session['popup_message'] = "Compra realizada com sucesso!"
        session['popup_type'] = "success"
    else:
        session['popup_message'] = "Saldo insuficiente ou investimento não encontrado."
        session['popup_type'] = "error"

    return redirect(url_for('investimento.investimento'))

@investimento_bp.route("/investimento/vender", methods=["POST"])
def vender():
    if 'user_info' not in session:
        return redirect(url_for('auth.login'))

    conta_id = session['user_info']['conta_id']
    investimento_id = request.form.get('investimento_id')

    quantidade_raw = request.form.get("quantidade")
    try:
        quantidade = int(quantidade_raw) if quantidade_raw else None
    except ValueError:
        quantidade = None

    if quantidade is None or quantidade <= 0:
        session['popup_message'] = "Quantidade inválida para venda."
        session['popup_type'] = "error"
        return redirect(url_for('investimento.investimento'))

    # Verifica quantidade na carteira
    conn = get_db()
    conn.row_factory = sqlite3.Row
    carteira_qtd_row = conn.execute(
        "SELECT quantidade FROM carteira_investimentos WHERE conta_id = ? AND investimento_id = ?",
        (conta_id, investimento_id),
    ).fetchone()
    conn.close()

    qtd_na_carteira = carteira_qtd_row["quantidade"] if carteira_qtd_row else 0
    if qtd_na_carteira <= 0:
        session['popup_message'] = "Você não possui este ativo na carteira."
        session['popup_type'] = "error"
        return redirect(url_for('investimento.investimento'))
    if quantidade > qtd_na_carteira:
        session['popup_message'] = "Quantidade para venda excede a quantidade que você possui."
        session['pop_type'] = "error"
        return redirect(url_for('investimento.investimento'))

    success = sell_investment(conta_id, investimento_id, quantidade)

    if success:
        session['popup_message'] = "Venda realizada com sucesso!"
        session['popup_type'] = "success"
    else:
        session['popup_message'] = "Não foi possível vender."
        session['popup_type'] = "error"

    return redirect(url_for('investimento.investimento'))


@investimento_bp.route("/investimento/atualizar-precos")
def atualizar_precos():
    """API única para retornar dados atualizados em tempo real."""
    if 'user_info' not in session:
        return jsonify({'error': 'Não autorizado'}), 401
    
    try:
        # CORREÇÃO: No seu sistema a chave é 'conta_id'
        conta_id = session['user_info'].get('conta_id')
        
        if not conta_id:
            return jsonify({'error': 'Conta não encontrada na sessão'}), 401

        # 1. Busca saldo atualizado do banco
        conn = get_db()
        conn.row_factory = sqlite3.Row
        conta = conn.execute("SELECT saldo FROM contas WHERE id = ?", (conta_id,)).fetchone()
        saldo_atual = conta['saldo'] if conta else 0
        conn.close()
        
        # 2. Busca carteira e ativos usando suas funções de serviço
        carteira_data = carregar_carteira(conta_id)
        carteira = carteira_data['investimentos'] if carteira_data else []
        
        investimentos_data = load_all_investiments()
        investimentos_disponiveis = investimentos_data['investimentos']
        
        return jsonify({
            'saldo': saldo_atual,
            'carteira': carteira,
            'ativos_disponiveis': investimentos_disponiveis
        })
        
    except Exception as e:
        print(f"Erro na API de preços: {e}")
        return jsonify({'error': str(e)}), 500
    
@investimento_bp.route("/investimento/detalhes/<int:investimento_id>")
def detalhes_investimento(investimento_id):
    """Retorna dados atualizados de um investimento para o modal."""
    if 'user_info' not in session:
        return jsonify({'error': 'Não autorizado'}), 401

    conta_id = session['user_info']['conta_id']
    conn = get_db()
    conn.row_factory = sqlite3.Row

    # Saldo da conta (dinheiro disponível)
    conta = conn.execute("SELECT saldo FROM contas WHERE id = ?", (conta_id,)).fetchone()
    saldo_conta = conta["saldo"] if conta else 0

    # Valor total atual da carteira (soma ao preço de mercado)
    valor_carteira_total = conn.execute("""
        SELECT COALESCE(SUM(ci.quantidade * i.valor_cota), 0) AS valor_total
        FROM carteira_investimentos ci
        JOIN investimentos i ON i.id = ci.investimento_id
        WHERE ci.conta_id = ?
    """, (conta_id,)).fetchone()["valor_total"]

    # Busca informações do investimento na carteira do usuário
    investimento = conn.execute("""
        SELECT 
            ci.quantidade,
            ci.preco_medio,
            i.nome,
            i.valor_cota as preco_atual,
            i.risco,
            i.descricao
        FROM carteira_investimentos ci
        JOIN investimentos i ON i.id = ci.investimento_id
        WHERE ci.conta_id = ? AND ci.investimento_id = ?
    """, (conta_id, investimento_id)).fetchone()

    if not investimento:
        # Se não estiver na carteira, pode ser que o usuário esteja explorando o ativo (compra)
        ativo = conn.execute("""
            SELECT id, nome, valor_cota, risco, descricao
            FROM investimentos
            WHERE id = ?
        """, (investimento_id,)).fetchone()
        if ativo:
            return jsonify({
                'tipo': 'explorar',
                'nome': ativo['nome'],
                'preco_atual': ativo['valor_cota'],
                'risco': ativo['risco'],
                'descricao': ativo['descricao'],
                'saldo_conta': saldo_conta,
                'valor_carteira_total': valor_carteira_total
            })
        else:
            return jsonify({'error': 'Investimento não encontrado'}), 404

    # Caso esteja na carteira
    saldo_total = investimento['quantidade'] * investimento['preco_atual']
    # Gasto_total considera o preço médio registrado na carteira:
    # o preço atual do ativo muda (valor_cota), mas o "custo" deve vir do preco_medio.
    gasto_total = investimento['preco_medio'] * investimento['quantidade']
    lucro_prejuizo = saldo_total - gasto_total

    return jsonify({
        'tipo': 'carteira',
        'investimento_id': investimento_id,
        'nome': investimento['nome'],
        'quantidade': investimento['quantidade'],
        'preco_medio': investimento['preco_medio'],
        'preco_atual': investimento['preco_atual'],
        'saldo_total': saldo_total,
        'lucro_prejuizo': lucro_prejuizo,
        'risco': investimento['risco'],
        'descricao': investimento['descricao'],
        'saldo_conta': saldo_conta,
        'valor_carteira_total': valor_carteira_total
    })