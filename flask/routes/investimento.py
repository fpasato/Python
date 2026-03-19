# routes/investimento.py
from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify, flash
from utils.services.banco.investimento import (
    listar_investimentos_ativos,
    comprar_investimento_db,
    vender_investimento_db,
    get_history_prices,
    carregar_carteira
)

investimento_bp = Blueprint("investimento", __name__)

@investimento_bp.route("/investimento")
def investimento():
    if "user_info" not in session:
        return redirect(url_for("auth.login"))
    
    conta_id = session["user_info"]["conta_id"]
    try:
        ativos = listar_investimentos_ativos()
        carteira = carregar_carteira(conta_id)
        valor_carteira = sum(item["quantidade"]*item["preco_medio"] for item in carteira) if carteira else 0
    except Exception as e:
        flash(f"Erro ao carregar investimentos: {str(e)}", "error")
        ativos, carteira, valor_carteira = [], [], 0

    return render_template(
        "investimento/index.html",
        ativos_disponiveis=ativos,
        carteira=carteira,
        valor_carteira=valor_carteira,
        session=session
    )


@investimento_bp.route("/investimento/comprar", methods=["POST"])
def comprar_investimento():
    if "user_info" not in session:
        return redirect(url_for("auth.login"))

    investimento_id = request.form.get("investimento_id")
    quantidade = request.form.get("quantidade")
    conta_id = session["user_info"]["conta_id"]

    if not investimento_id or not quantidade:
        flash("Dados incompletos para compra.", "error")
        return redirect(url_for("investimento.investimento"))

    try:
        quantidade = float(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade inválida")
        valor_total = comprar_investimento_db(conta_id, investimento_id, quantidade)
        flash(f"Compra realizada: {quantidade} cotas por R$ {valor_total:.2f}", "success")
    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("investimento.investimento"))


@investimento_bp.route("/investimento/vender", methods=["POST"])
def vender_investimento():
    if "user_info" not in session:
        return redirect(url_for("auth.login"))

    investimento_id = request.form.get("investimento_id")
    quantidade = request.form.get("quantidade")
    conta_id = session["user_info"]["conta_id"]

    if not investimento_id or not quantidade:
        flash("Dados incompletos para venda.", "error")
        return redirect(url_for("investimento.investimento"))

    try:
        quantidade = float(quantidade)
        if quantidade <= 0:
            raise ValueError("Quantidade inválida")
        valor_venda = vender_investimento_db(conta_id, investimento_id, quantidade)
        flash(f"Venda realizada: {quantidade} cotas por R$ {valor_venda:.2f}", "success")
    except Exception as e:
        flash(str(e), "error")

    return redirect(url_for("investimento.investimento"))


@investimento_bp.route("/investimento/historico/<int:investimento_id>")
def historico_json(investimento_id):
    try:
        history = get_history_prices(investimento_id, limit=30)
        dados = [{"data": h["data"], "preco": h["preco"]} for h in history]
        return jsonify(dados)
    except Exception as e:
        flash(f"Erro ao carregar histórico: {str(e)}", "error")
        return redirect(url_for("investimento.investimento"))