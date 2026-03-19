# utils/services/banco/investimento.py
import random, time, threading
from datetime import datetime, timedelta
from utils.validators import get_db

# ----------------- Investimentos -----------------
def inserir_investimento(nome, descricao, valor_cota, imagem, risco, ativo=1):
    conn = get_db()
    conn.execute("""
        INSERT INTO investimentos (nome, descricao, valor_cota, imagem, risco, ativo)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, descricao, valor_cota, imagem, risco, ativo))
    conn.commit()
    conn.close()

def listar_investimentos_ativos():
    conn = get_db()
    ativos = conn.execute("SELECT * FROM investimentos WHERE ativo=1").fetchall()
    conn.close()
    return ativos

def get_investimento_by_id(investimento_id):
    conn = get_db()
    invest = conn.execute("SELECT * FROM investimentos WHERE id=?", (investimento_id,)).fetchone()
    conn.close()
    return invest

# ----------------- Carteira -----------------
def carregar_carteira(conta_id):
    conn = get_db()
    carteira = conn.execute("""
        SELECT ci.*, i.nome, i.imagem, i.risco
        FROM carteira_investimentos ci
        JOIN investimentos i ON i.id = ci.investimento_id
        WHERE ci.conta_id = ?
    """, (conta_id,)).fetchall()
    conn.close()
    return carteira

def comprar_investimento_db(conta_id, investimento_id, quantidade):
    conn = get_db()
    cursor = conn.cursor()
    try:
        ativo = cursor.execute("SELECT valor_cota FROM investimentos WHERE id=?", (investimento_id,)).fetchone()
        preco = ativo["valor_cota"]
        valor_total = preco * quantidade
        conta = cursor.execute("SELECT saldo FROM contas WHERE id=?", (conta_id,)).fetchone()
        if conta["saldo"] < valor_total:
            raise ValueError("Saldo insuficiente")
        cursor.execute("UPDATE contas SET saldo=saldo-? WHERE id=?", (valor_total, conta_id))
        existente = cursor.execute("SELECT * FROM carteira_investimentos WHERE conta_id=? AND investimento_id=?", (conta_id, investimento_id)).fetchone()
        if existente:
            cursor.execute("UPDATE carteira_investimentos SET quantidade=? WHERE id=?", (existente["quantidade"]+quantidade, existente["id"]))
        else:
            cursor.execute("INSERT INTO carteira_investimentos (conta_id, investimento_id, quantidade, preco_medio) VALUES (?,?,?,?)", (conta_id, investimento_id, quantidade, preco))
        conn.commit()
        return valor_total
    finally:
        conn.close()

def vender_investimento_db(conta_id, investimento_id, quantidade):
    conn = get_db()
    cursor = conn.cursor()
    try:
        existente = cursor.execute("SELECT * FROM carteira_investimentos WHERE conta_id=? AND investimento_id=?", (conta_id, investimento_id)).fetchone()
        if not existente or existente["quantidade"] < quantidade:
            raise ValueError("Quantidade insuficiente")
        preco = cursor.execute("SELECT valor_cota FROM investimentos WHERE id=?", (investimento_id,)).fetchone()["valor_cota"]
        valor_venda = quantidade * preco
        cursor.execute("UPDATE contas SET saldo=saldo+? WHERE id=?", (valor_venda, conta_id))
        nova_qtd = existente["quantidade"] - quantidade
        if nova_qtd > 0:
            cursor.execute("UPDATE carteira_investimentos SET quantidade=? WHERE id=?", (nova_qtd, existente["id"]))
        else:
            cursor.execute("DELETE FROM carteira_investimentos WHERE id=?", (existente["id"],))
        conn.commit()
        return valor_venda
    finally:
        conn.close()

# ----------------- Histórico -----------------
def seed_historico(investimento_id, dias=20, preco_inicial=25.0):
    conn = get_db()
    base_date = datetime.now() - timedelta(days=dias)
    preco = preco_inicial
    for i in range(dias):
        preco = round(preco*(1+random.uniform(-0.02,0.02)),2)
        data = (base_date + timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("INSERT INTO historico_precos (investimento_id, data, preco) VALUES (?,?,?)", (investimento_id, data, preco))
    conn.commit()
    conn.close()

def get_history_prices(investimento_id, limit=30):
    conn = get_db()
    history = conn.execute("SELECT data, preco FROM historico_precos WHERE investimento_id=? ORDER BY data ASC LIMIT ?", (investimento_id, limit)).fetchall()
    conn.close()
    return history

def atualizar_precos():
    conn = get_db()
    ativos = conn.execute("SELECT id, valor_cota, risco FROM investimentos WHERE ativo=1").fetchall()
    for a in ativos:
        ultimo = conn.execute("SELECT preco FROM historico_precos WHERE investimento_id=? ORDER BY data DESC LIMIT 1", (a["id"],)).fetchone()
        base = ultimo["preco"] if ultimo else a["valor_cota"]
        vol = {"alto":0.05,"medio":0.03,"baixo":0.01}.get(a["risco"],0.02)
        novo_preco = round(base*(1+random.uniform(-vol, vol)),2)
        conn.execute("INSERT INTO historico_precos (investimento_id, preco) VALUES (?,?)", (a["id"], novo_preco))
        conn.execute("UPDATE investimentos SET valor_cota=? WHERE id=?", (novo_preco, a["id"]))
    conn.commit()
    conn.close()

# ----------------- Simulação -----------------
_simulacao_ativa=False
def iniciar_simulacao(intervalo=60):
    global _simulacao_ativa
    if _simulacao_ativa: return
    _simulacao_ativa=True
    def loop():
        while _simulacao_ativa:
            atualizar_precos()
            time.sleep(intervalo)
    threading.Thread(target=loop, daemon=True).start()