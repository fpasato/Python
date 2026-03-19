from utils.validators import *
from utils.validators import get_db

def confirmarTransferencia(conta_origem_id, conta_destino_id, valor):
    
    conn = get_db()
    cursor = conn.cursor()
    
    # saldo origem
    cursor.execute("SELECT saldo FROM contas WHERE id = ?", (conta_origem_id,))
    saldo_origem = cursor.fetchone()[0]
    
    if saldo_origem < valor:
        conn.close()
        return {
            "success": False,
            "message": "Saldo insuficiente"
        }
    
    try:
        with conn:
            # saída
            cursor.execute("""
                UPDATE contas 
                SET saldo = saldo - ?
                WHERE id = ?
            """, (valor, conta_origem_id))
            
            cursor.execute("""
                INSERT INTO transacoes_conta (conta_id, tipo, valor, descricao)
                VALUES (?, 'saida', ?, 'Transferência enviada')
            """, (conta_origem_id, valor))
            
            # entrada
            cursor.execute("""
                UPDATE contas 
                SET saldo = saldo + ?
                WHERE id = ?
            """, (valor, conta_destino_id))
            
            cursor.execute("""
                INSERT INTO transacoes_conta (conta_id, tipo, valor, descricao)
                VALUES (?, 'entrada', ?, 'Transferência recebida de ' || (SELECT nome_completo FROM usuarios WHERE id = ?))
            """, (conta_destino_id, valor, conta_origem_id))

        return {
            "success": True,
            "message": "Transferência realizada com sucesso"
        }

    except Exception as e:
        print("ERRO REAL:", e)  
        return {
            "success": False,
            "message": "Erro na transferência"
        }