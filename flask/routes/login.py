# routes/investimento.py
from flask import Blueprint, render_template, session, request
from utils.services.banco.investimento import (
    listar_investimentos_ativos,
    comprar_investimento_db,
    vender_investimento_db,
    get_history_prices,
    carregar_carteira
)

investimento_bp = Blueprint("investimento", __name__)

@investimento_bp.route("/investimento", methods=["GET", "POST"])
def investimento():
    if "user_info" not in session:
        return redirect("/login")

    conta_id = session["user_info"]["conta_id"]
    popup_message = None
    popup_type = None

    try:
        ativos = listar_investimentos_ativos()
        carteira = carregar_carteira(conta_id)
        valor_carteira = sum(item["quantidade"]*item["preco_medio"] for item in carteira) if carteira else 0
    except Exception as e:
        ativos, carteira, valor_carteira = [], [], 0
        popup_message = f"Erro ao carregar investimentos: {str(e)}"
        popup_type = "error"

    return render_template(
        "investimento/index.html",
        ativos_disponiveis=ativos,
        carteira=carteira,
        valor_carteira=valor_carteira,
        session=session,
        popup_message=popup_message,
        popup_type=popup_type
    )


@investimento_bp.route("/investimento/comprar", methods=["POST"])
def comprar_investimento():
    if "user_info" not in session:
        return redirect("/login")

    conta_id = session["user_info"]["conta_id"]
    investimento_id = request.form.get("investimento_id")
    quantidade = request.form.get("quantidade")
    popup_message = None
    popup_type = None

    if not investimento_id or not quantidade:
        popup_message = "Preencha todos os campos da compra"
        popup_type = "error"
    else:
        try:
            quantidade = float(quantidade)
            if quantidade <= 0:
                raise ValueError("Quantidade inválida")
            valor_total = comprar_investimento_db(conta_id, investimento_id, quantidade)
            popup_message = f"Compra realizada: {quantidade} cotas por R$ {valor_total:.2f}"
            popup_type = "success"
        except Exception as e:
            popup_message = str(e)
            popup_type = "error"

    # Recarrega ativos e carteira para renderizar a mesma página
    ativos = listar_investimentos_ativos()
    carteira = carregar_carteira(conta_id)
    valor_carteira = sum(item["quantidade"]*item["preco_medio"] for item in carteira) if carteira else 0

    return render_template(
        "investimento/index.html",
        ativos_disponiveis=ativos,
        carteira=carteira,
        valor_carteira=valor_carteira,
        session=session,
        popup_message=popup_message,
        popup_type=popup_type
    )


@investimento_bp.route("/investimento/vender", methods=["POST"])
def vender_investimento():
    if "user_info" not in session:
        return redirect("/login")

    conta_id = session["user_info"]["conta_id"]
    investimento_id = request.form.get("investimento_id")
    quantidade = request.form.get("quantidade")
    popup_message = None
    popup_type = None

    if not investimento_id or not quantidade:
        popup_message = "Preencha todos os campos da venda"
        popup_type = "error"
    else:
        try:
            quantidade = float(quantidade)
            if quantidade <= 0:
                raise ValueError("Quantidade inválida")
            valor_venda = vender_investimento_db(conta_id, investimento_id, quantidade)
            popup_message = f"Venda realizada: {quantidade} cotas por R$ {valor_venda:.2f}"
            popup_type = "success"
        except Exception as e:
            popup_message = str(e)
            popup_type = "error"

    ativos = listar_investimentos_ativos()
    carteira = carregar_carteira(conta_id)
    valor_carteira = sum(item["quantidade"]*item["preco_medio"] for item in carteira) if carteira else 0

    return render_template(
        "investimento/index.html",
        ativos_disponiveis=ativos,
        carteira=carteira,
        valor_carteira=valor_carteira,
        session=session,
        popup_message=popup_message,
        popup_type=popup_type
    )


@investimento_bp.route("/investimento/historico/<int:investimento_id>")
def historico_json(investimento_id):
    try:
        history = get_history_prices(investimento_id, limit=30)
        dados = [{"data": h["data"], "preco": h["preco"]} for h in history]
        return jsonify(dados)
    except Exception as e:
        # Renderiza a página principal com erro
        conta_id = session["user_info"]["conta_id"]
        ativos = listar_investimentos_ativos()
        carteira = carregar_carteira(conta_id)
        valor_carteira = sum(item["quantidade"]*item["preco_medio"] for item in carteira) if carteira else 0
        return render_template(
            "investimento/index.html",
            ativos_disponiveis=ativos,
            carteira=carteira,
            valor_carteira=valor_carteira,
            session=session,
            popup_message=f"Erro ao carregar histórico: {str(e)}",
            popup_type="error"
        )