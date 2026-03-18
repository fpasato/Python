from utils.validators import *




def confirmarTransferencia(conta_origem, conta_destino, valor):
    
    if conta_origem['saldo'] < valor:
        return {
            "success": False,
            "message": "Saldo insuficiente"
        }

    conn = get_db()
    cursor = conn.cursor()
    
    try:
        with conn:
            # saída
            cursor.execute("""
                UPDATE contas 
                SET saldo = saldo - ?
                WHERE id = ?
            """, (valor, conta_origem['id']))
            
            cursor.execute("""
                INSERT INTO transacoes (conta_id, tipo, valor, descricao)
                VALUES (?, 'saida', ?, 'Transferência enviada')
            """, (conta_origem['id'], valor))
            
            # entrada
            cursor.execute("""
                UPDATE contas 
                SET saldo = saldo + ?
                WHERE id = ?
            """, (valor, conta_destino['id']))
            
            cursor.execute("""
                INSERT INTO transacoes (conta_id, tipo, valor, descricao)
                VALUES (?, 'entrada', ?, 'Transferência recebida')
            """, (conta_destino['id'], valor))

        return {
            "success": True,
            "message": "Transferência realizada com sucesso"
        }

    except Exception as e:
        return {
            "success": False,
            "message": "Erro na transferência"
        }