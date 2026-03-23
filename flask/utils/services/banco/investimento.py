from datetime import datetime, timedelta
import random
import sqlite3
from utils.validators import get_db
from threading import Lock

notificacoes_pendentes = {}
notificacoes_lock = Lock()

import time

def carregar_carteira(conta_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    
    # 🔥 TESTE DEFINITIVO - Verificar estrutura
    tabelas = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print("=== TABELAS DO BANCO ===")
    print(tabelas)
    
    colunas = conn.execute("PRAGMA table_info(investimentos_temporarios)").fetchall()
    print("=== COLUNAS DE investimentos_temporarios ===")
    print(colunas)
    
    agora = int(time.time() * 1000)  # ms
    
    temporarios = conn.execute("""
        SELECT 
            it.id as id,
            it.quantidade,
            it.preco_medio,
            i.nome,
            i.valor_cota as preco_atual,
            1 as temporario,
            it.tempo_inicio,
            it.duracao
        FROM investimentos_temporarios it
        JOIN investimentos i ON i.id = it.investimento_id
        WHERE it.conta_id = ?
        AND (it.tempo_inicio + it.duracao) > ?
    """, (conta_id, agora)).fetchall()

    if not temporarios:
        conn.close()
        return {'id_conta': conta_id, 'investimentos': []}

    carteira_lista = []
    for row in temporarios:
        invest = dict(row)

        invest['saldo'] = invest['preco_medio'] * invest['quantidade']
        valor_mercado = invest['quantidade'] * invest['preco_atual']
        invest['lucro_prejuizo'] = valor_mercado - invest['saldo']

        # 🔥 calcula tempo restante já pronto pro frontend
        invest['tempo_restante'] = invest['duracao'] - (agora - invest['tempo_inicio'])

        carteira_lista.append(invest)

    conn.close()
    return {'id_conta': conta_id, 'investimentos': carteira_lista}


def load_investiment(investimento_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    investimento = conn.execute("""
        SELECT id, nome, descricao, valor_cota, risco, ativo
        FROM investimentos
        WHERE id = ? AND ativo = 1
    """, (investimento_id,)).fetchone()
    conn.close()
    if investimento:
        print(f"DEBUG: Investimento encontrado: {dict(investimento)}")
    else:
        print(f"DEBUG: Investimento {investimento_id} não encontrado ou inativo")
    return dict(investimento) if investimento else None

def load_all_investiments():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    investimentos = conn.execute("""
        SELECT id, nome, descricao, valor_cota, risco, ativo
        FROM investimentos
        WHERE ativo = 1
    """).fetchall()
    conn.close()
    return {'investimentos': [dict(row) for row in investimentos]}


def buy_investment(conta_id, investimento_id, quantidade, tempo):
    conn = get_db()
    conn.row_factory = sqlite3.Row

    conta = conn.execute("SELECT saldo FROM contas WHERE id = ?", (conta_id,)).fetchone()
    if not conta:
        print("DEBUG: Conta não encontrada")
        conn.close()
        return False

    saldo_real = conta['saldo']
    ativo = load_investiment(investimento_id)

    print(f"DEBUG: Conta {conta_id} saldo = {saldo_real}")
    print(f"DEBUG: Investimento {investimento_id} encontrado? {ativo is not None}")

    try:
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        print("DEBUG: Quantidade inválida")
        conn.close()
        return False

    if quantidade <= 0:
        print("DEBUG: Quantidade deve ser maior que 0")
        conn.close()
        return False

    if not ativo:
        print("DEBUG: Ativo não encontrado")
        conn.close()
        return False

    valor_total = ativo['valor_cota'] * quantidade
    preco_medio = valor_total / quantidade 
    
    if saldo_real < valor_total:
        print(f"DEBUG: Saldo insuficiente: {saldo_real} < {valor_total}")
        conn.close()
        return False

    if tempo:
        tempo_inicio = int(time.time() * 1000)  # ms
        duracao = int(tempo)  
        print(f"DEBUG: buy_investment - tempo = {tempo}, type = {type(tempo)}")
        conn.execute("""
            INSERT INTO investimentos_temporarios 
            (conta_id, investimento_id, quantidade, preco_medio, tempo_inicio, duracao)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (conta_id, investimento_id, quantidade, preco_medio, tempo_inicio, duracao))

    conn.execute("UPDATE contas SET saldo = saldo - ? WHERE id = ?", (valor_total, conta_id))
    conn.commit()
    conn.close()
    return True


def history_prices(investimento_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    history = conn.execute("""
        SELECT data, preco
        FROM historico_precos
        WHERE investimento_id = ?
        ORDER BY data ASC
        LIMIT 10
    """, (investimento_id,)).fetchall()
    conn.close()
    return [dict(row) for row in history]

def remover_ativo_para_todos(investimento_id, conn):
    # (não necessário para temporários)
    pass

def vender_ativo_para_todos(investimento_id, conn):
    # (não necessário para temporários)
    pass

def atualizar_ativos():
    # (mantenha como estava, sem alterações)
    pass

def busca_investimento_temporarios():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    agora = int(time.time() * 1000)
    print(f"DEBUG: Busca expirados - agora={agora}")
    expirados = conn.execute("""
        SELECT * FROM investimentos_temporarios
        WHERE (tempo_inicio + duracao) <= ?
    """, (agora,)).fetchall()
    print(f"DEBUG: Encontrados {len(expirados)} expirados")
    conn.close()
    return [dict(row) for row in expirados]


def processar_investimentos_expirados():
    expirados = busca_investimento_temporarios()
    conn = get_db()
    agora = int(time.time() * 1000) 
    for inv in expirados:
        print(f"DEBUG: Processando expirado id={inv['id']}, conta={inv['conta_id']}, investimento={inv['investimento_id']}, tempo_inicio={inv['tempo_inicio']}, duracao={inv['duracao']}, expira_em={inv['tempo_inicio']+inv['duracao']}, agora={agora}")
        conta_id = inv["conta_id"]
        investimento_id = inv["investimento_id"]
        quantidade = inv["quantidade"]
        preco_medio = inv["preco_medio"]
        temp_id = inv["id"]
        ativo = conn.execute("SELECT nome, valor_cota FROM investimentos WHERE id = ?", (investimento_id,)).fetchone()
        if not ativo:
            continue
        preco_atual = ativo["valor_cota"]
        valor_venda = quantidade * preco_atual
        custo_total = quantidade * preco_medio
        lucro = valor_venda - custo_total
        # Atualiza o saldo do usuário
        conn.execute("UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor_venda, conta_id))
        conn.execute("DELETE FROM investimentos_temporarios WHERE id = ?", (temp_id,))
        notificacao = {
            'tipo': 'venda_automatica',
            'nome': ativo['nome'],
            'quantidade': quantidade,
            'lucro': lucro,
            'preco_venda': preco_atual,
            'preco_medio': preco_medio
        }
        with notificacoes_lock:
            notificacoes_pendentes.setdefault(conta_id, []).append(notificacao)
        conn.commit()
    conn.close()