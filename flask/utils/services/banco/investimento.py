


from datetime import datetime, timedelta, timezone
import random
import sqlite3
from utils.validators import get_db
from threading import Lock

notificacoes_pendentes = {}     
notificacoes_lock = Lock()

#carrega carteira
def carregar_carteira(conta_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    
    carteira = conn.execute("""
        SELECT 
            ci.investimento_id,
            ci.quantidade,
            ci.preco_medio,
            i.nome,
            i.valor_cota as preco_atual
        FROM carteira_investimentos ci
        JOIN investimentos i ON i.id = ci.investimento_id
        WHERE ci.conta_id = ?
    """, (conta_id,)).fetchall()
    
    if not carteira:
        return {'id_conta': conta_id, 'investimentos': []}
    
    carteira_lista = []
    for row in carteira:
        invest = dict(row)
        # Valor total investido (preço médio × quantidade)
        invest['saldo'] = invest['preco_medio'] * invest['quantidade']
        # Valor de mercado atual (quantidade × preço atual)
        valor_mercado = invest['quantidade'] * invest['preco_atual']
        # Lucro/prejuízo em relação ao preço médio
        invest['lucro_prejuizo'] = valor_mercado - invest['saldo']
        carteira_lista.append(invest)
    
    conn.close()
    return {'id_conta': conta_id, 'investimentos': carteira_lista}


def load_investiment(investimento_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    
    investimento = conn.execute("""
        SELECT 
            id,
            nome,
            descricao,
            valor_cota,
            risco,
            ativo
        FROM investimentos
        WHERE id = ? AND ativo = 1
    """, (investimento_id,)).fetchone()
    
    if not investimento:
        return None
    
    # Converte para dicionário
    investimento_dict = dict(investimento)
    
    conn.close()
    return investimento_dict



def load_all_investiments():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    
    investimentos = conn.execute("""
        SELECT 
            id,
            nome,
            descricao,
            valor_cota,
            risco,
            ativo
        FROM investimentos
        WHERE ativo = 1
    """).fetchall()
    
    # Converte para lista de dicionários
    investimentos_lista = [dict(row) for row in investimentos]
    
    # Monta o dicionário final
    investimentos_info = {
        'investimentos': investimentos_lista
    }
    
    conn.close()
    return investimentos_info



def sell_investment(conta_id, investimento_id, quantidade=None):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    
    # 1. Pega a quantidade que o usuário tem
    carteira = conn.execute("SELECT quantidade FROM carteira_investimentos WHERE conta_id = ? AND investimento_id = ?", (conta_id, investimento_id)).fetchone()
    # 2. Pega o preço ATUAL do mercado
    ativo = conn.execute("SELECT valor_cota FROM investimentos WHERE id = ?", (investimento_id,)).fetchone()
    
    if not carteira or not ativo:
        return False
    
    qtd_na_carteira = carteira["quantidade"]
    if quantidade is None:
        quantidade = qtd_na_carteira
    try:
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        conn.close()
        return False
    
    # Venda parcial (quantidade positiva e <= quantidade em carteira)
    if quantidade <= 0 or quantidade > qtd_na_carteira:
        conn.close()
        return False
    
    valor_venda_total = quantidade * ativo["valor_cota"]
    
    # Adiciona o valor de MERCADO ao saldo
    conn.execute("UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor_venda_total, conta_id))
    
    # Atualiza/Remove da carteira
    restante = qtd_na_carteira - quantidade
    if restante <= 0:
        conn.execute(
            "DELETE FROM carteira_investimentos WHERE conta_id = ? AND investimento_id = ?",
            (conta_id, investimento_id),
        )
    else:
        # Mantém preco_medio (média ponderada) ao reduzir quantidade
        conn.execute(
            "UPDATE carteira_investimentos SET quantidade = ? WHERE conta_id = ? AND investimento_id = ?",
            (restante, conta_id, investimento_id),
        )
    
    conn.commit()
    conn.close()
    return True

def buy_investment(conta_id, investimento_id, quantidade, tempo=None):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    
    # BUSCA SALDO REAL DO BANCO, NÃO DA SESSÃO
    conta = conn.execute("SELECT saldo FROM contas WHERE id = ?", (conta_id,)).fetchone()
    if not conta:
        conn.close()
        return False
        
    saldo_real = conta['saldo']
    ativo = load_investiment(investimento_id)
    
    # tenta converter quantidade para int
    try:
        quantidade = int(quantidade)
    except (TypeError, ValueError):
        conn.close()
        return False
    
    # se quantidade for menor ou igual a 0
    if quantidade <= 0:
        conn.close()
        return False
    
    # se ativo não existir ou saldo insuficiente
    if not ativo or saldo_real < (ativo['valor_cota'] * quantidade):
        conn.close()
        return False
    
    valor_total = ativo['valor_cota'] * quantidade

    try:
        investimento = conn.execute(
            "SELECT quantidade, preco_medio FROM carteira_investimentos WHERE conta_id = ? AND investimento_id = ?",
            (conta_id, investimento_id)
        ).fetchone()
        
        if investimento:
            nova_qtd = investimento['quantidade'] + quantidade
            novo_pm = ((investimento['preco_medio'] * investimento['quantidade']) + valor_total) / nova_qtd
            conn.execute(
                "UPDATE carteira_investimentos SET quantidade = ?, preco_medio = ? WHERE conta_id = ? AND investimento_id = ?",
                (nova_qtd, novo_pm, conta_id, investimento_id)
            )
        else:
            conn.execute(
                "INSERT INTO carteira_investimentos (conta_id, investimento_id, quantidade, preco_medio) VALUES (?, ?, ?, ?)",
                (conta_id, investimento_id, quantidade, valor_total / quantidade)
            )

        tempo = int(tempo) if tempo else None

        if tempo:
            expira_em = datetime.utcnow() + timedelta(seconds=tempo)
            expira_em_str = expira_em.strftime('%Y-%m-%d %H:%M:%S')

            conn.execute("""
                INSERT INTO investimentos_temporarios 
                (conta_id, investimento_id, quantidade, preco_medio, expira_em)
                VALUES (?, ?, ?, ?, ?)
            """, (conta_id, investimento_id, quantidade, valor_total / quantidade, expira_em_str))

        conn.execute(
            "UPDATE contas SET saldo = saldo - ? WHERE id = ?",
            (valor_total, conta_id)
        )

        conn.commit()
        return True

    except Exception as e:
        print(f"Erro na transação: {e}")
        return False

    finally:
        conn.close()



def history_prices(investimento_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    
    history = conn.execute("""
        SELECT 
            data,
            preco
        FROM historico_precos
        WHERE investimento_id = ?
        ORDER BY data ASC
        LIMIT 10
    """, (investimento_id,)).fetchall()
    
    # Converte para lista de dicionários
    history_lista = [dict(row) for row in history]
    
    conn.close()
    return history_lista



def remover_ativo_para_todos(investimento_id, conn):
    """Remove todas as cotas deste ativo da carteira de todos os usuários
       sem devolver dinheiro (perda total do investimento).
       O ativo permanece ativo para novas compras."""
    carteiras = conn.execute("""
        SELECT conta_id, quantidade
        FROM carteira_investimentos
        WHERE investimento_id = ?
    """, (investimento_id,)).fetchall()

    if not carteiras:
        return

    for item in carteiras:
        conta_id = item["conta_id"]
        quantidade = item["quantidade"]
        
        # Apenas remove da carteira, não devolve dinheiro
        conn.execute("""
            DELETE FROM carteira_investimentos
            WHERE conta_id = ? AND investimento_id = ?
        """, (conta_id, investimento_id))

    # Commit to ensure all deletions are saved
    conn.commit()
    print(f"[{datetime.now()}] Ativo {investimento_id} removido da carteira de {len(carteiras)} usuários (perda total). Ativo permanece disponível.")


def vender_ativo_para_todos(investimento_id, conn):
    """Vende todas as cotas deste ativo para todos os usuários que o possuem,
       creditando o valor atual (que será 1) e removendo da carteira.
       O ativo permanece ativo para novas compras."""
    carteiras = conn.execute("""
        SELECT conta_id, quantidade
        FROM carteira_investimentos
        WHERE investimento_id = ?
    """, (investimento_id,)).fetchall()

    if not carteiras:
        return

    for item in carteiras:
        conta_id = item["conta_id"]
        quantidade = item["quantidade"]
        valor_venda = quantidade * 1  # preço de venda fixado em 1

        conn.execute("""
            UPDATE contas
            SET saldo = saldo + ?
            WHERE id = ?
        """, (valor_venda, conta_id))

        conn.execute("""
            DELETE FROM carteira_investimentos
            WHERE conta_id = ? AND investimento_id = ?
        """, (conta_id, investimento_id))

    # Commit the transaction to ensure all deletions are saved
    conn.commit()
    print(f"[{datetime.now()}] Ativo {investimento_id} vendido automaticamente para {len(carteiras)} usuários com prejuízo. Ativo permanece disponível.")


def atualizar_ativos():
    conn = get_db()
    conn.row_factory = sqlite3.Row

    # Verifica se já atualizou recentemente (opcional)
    ultimo = conn.execute("SELECT MAX(ultimo_update) as last FROM investimentos").fetchone()["last"]
    if ultimo:
        ultimo = datetime.fromisoformat(ultimo)
        if datetime.now() - ultimo < timedelta(seconds=25):
            print("Já atualizado recentemente")
            conn.close()
            return

    ativos = conn.execute("SELECT id, valor_cota, risco FROM investimentos WHERE ativo = 1").fetchall()

    for ativo in ativos:
        valor = ativo["valor_cota"]
        risco = ativo["risco"]
        
        # tendência leve
        tendencia = random.uniform(-0.001, 0.002)

        # ruído (volatilidade)
        if risco == "baixo":
            ruido = random.uniform(-0.001, 0.002)
        elif risco == "medio":
            ruido = random.uniform(-0.002, 0.003)
        else:
            ruido = random.uniform(-0.004, 0.006)

        # retorno à média (corrigido)
        preco_base = 100
        retorno = (preco_base - valor) * 0.0003

        variacao = tendencia + ruido + retorno

        novo_valor = round(valor * (1 + variacao), 2)
    
        if novo_valor <= 1:
            print(f"Ativo {ativo['id']} atingiu R$1 - removendo da carteira sem reembolso")
            novo_valor = 1
            remover_ativo_para_todos(ativo["id"], conn)

        conn.execute(
            "UPDATE investimentos SET valor_cota = ? WHERE id = ?",
            (novo_valor, ativo["id"])
        )

        # Registra no histórico para o gráfico (últimos 30 são retornados pela API)
        conn.execute(
            "INSERT INTO historico_precos (investimento_id, preco) VALUES (?, ?)",
            (ativo["id"], novo_valor),
        )

    agora = datetime.now().isoformat()
    conn.execute("UPDATE investimentos SET ultimo_update = ?", (agora,))
    conn.commit()
    conn.close()

    print(f"[{datetime.now()}] Ativos atualizados")
    
    


# ----------------------------------------------------------------------

def busca_investimento_temporarios():
    """Retorna investimentos temporários já expirados."""
    conn = get_db()
    conn.row_factory = sqlite3.Row
    expirados = conn.execute("""
        SELECT * FROM investimentos_temporarios
        WHERE expira_em <= datetime('now', 'utc')
    """).fetchall()
    conn.close()
    return [dict(row) for row in expirados]




def processar_investimentos_expirados():
    expirados = busca_investimento_temporarios()
    conn = get_db()

    for inv in expirados:
        conta_id = inv["conta_id"]
        investimento_id = inv["investimento_id"]
        quantidade = inv["quantidade"]
        preco_medio = inv["preco_medio"]   # já está na tabela
        temp_id = inv["id"]

        # Busca nome e preço atual do ativo
        ativo = conn.execute(
            "SELECT nome, valor_cota FROM investimentos WHERE id = ?", (investimento_id,)
        ).fetchone()
        if not ativo:
            continue

        preco_atual = ativo["valor_cota"]
        valor_venda = quantidade * preco_atual
        custo_total = quantidade * preco_medio
        lucro = valor_venda - custo_total

        sucesso = sell_investment(conta_id, investimento_id, quantidade)

        if sucesso:
            conn.execute("DELETE FROM investimentos_temporarios WHERE id = ?", (temp_id,))
            
            # Prepara notificação estruturada
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
        else:
            # Falha na venda – mantém registro
            pass

    conn.close()
    
    
    
def _obter_nome_investimento(investimento_id, conn):
    row = conn.execute(
        "SELECT nome FROM investimentos WHERE id = ?", (investimento_id,)
    ).fetchone()
    return row["nome"] if row else f"#{investimento_id}"