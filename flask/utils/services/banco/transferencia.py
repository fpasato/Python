from utils.validators import *


def confirmarTransferencia(conta_usuario, conta_destino, valor):
    
    if not conta_usuario['saldo'] >= valor:
        return {"success": False, "message": "Saldo insuficiente"}
    
    conta_usuario['saldo'] -= valor
    conta_destino['saldo'] += valor
    
    db = get_db()
    with db:
        db.execute(
            "UPDATE contas SET saldo = ? WHERE numero_conta = ?",
            (conta_usuario['saldo'], conta_usuario['numero_conta'])
        )
        db.execute(
            "UPDATE contas SET saldo = ? WHERE numero_conta = ?",
            (conta_destino['saldo'], conta_destino['numero_conta'])
        )
    
    return {"success": True, "message": "Transferência realizada com sucesso"}