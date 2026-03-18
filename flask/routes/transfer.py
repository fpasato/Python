from flask import Blueprint, request, session, render_template
from flask import redirect, url_for
from utils.validators import get_account_by_number, get_account_by_id
from utils.services.banco.transferencia import confirmarTransferencia

transfer_bp = Blueprint("transfer", __name__, url_prefix="/transfer")

@transfer_bp.route("/", methods=["GET", "POST"])
def transfer():
    
    conta_usuario = get_account_by_id(session['user_info']['user_id'])
    if request.method == "GET":
        return render_template(
            "transfer/index.html",
            nome_usuario=session['user_info']['user_name'],
            conta_usuario=conta_usuario,  
            conta_destino_info=None
        )

    elif request.method == "POST":
        
        acao = request.form.get("acao")
        
        #se a ação for buscar conta destino
        if acao == "buscar":
            conta_destino_num = request.form.get("conta-destino")
            conta = get_account_by_number(conta_destino_num)
            
            # se a conta não existir
            if not conta:
                return render_template(
                    "transfer/index.html",
                    popup_message="Conta destino não encontrada",
                    popup_type="error", 
                    conta_destino_info=None
                )
            # se a conta for igual a conta do usuário
            if conta['numero_conta'] == conta_usuario['numero_conta']:
                return render_template(
                    "transfer/index.html",
                    popup_message="Não é possível transferir para a própria conta",
                    popup_type="error",
                    conta_destino_info=None
                )
            
            # se a conta existir e for diferente da conta do usuário
            conta_destino_info = {
                "nome": conta['nome_completo'],
                "numero_conta": conta['numero_conta'],
                "agencia": "0010",
                "saldo": conta['saldo']  
            }
            
            return render_template(
                "transfer/index.html",
                nome_usuario=session['user_info']['user_name'],
                conta_usuario=conta_usuario, 
                conta_destino_info=conta_destino_info
            )
        
        valor = request.form.get("valor")
        
        resultado = confirmarTransferencia(conta_usuario, conta_destino_info, float(valor))
        
        if resultado["success"]:
            return render_template(
                "transfer/index.html",
                nome_usuario=session['user_info']['user_name'],
                conta_usuario=conta_usuario, 
                conta_destino_info=conta_destino_info,  
                popup_message=resultado["message"],
                popup_type="success"
            )
        else:
            return render_template(
                "transfer/index.html",
                nome_usuario=session['user_info']['user_name'],
                conta_usuario=conta_usuario, 
                conta_destino_info=conta_destino_info, 
                popup_message="Ocorreu um erro na transferência",
                popup_type="error"
            )


@transfer_bp.route("/transferir", methods=["POST"])
def transferir():
    
    conta_usuario = get_account_by_id(session['user_info']['user_id'])
    conta_destino_num = request.form.get("conta-destino-final")
    valor = float(request.form.get("valor"))
    
    conta_destino = get_account_by_number(conta_destino_num)
    
    if not conta_destino:
        return render_template(
            "transfer/index.html",
            nome_usuario=session['user_info']['user_name'],
            conta_usuario=conta_usuario, 
            popup_message="Conta destino não encontrada",
            popup_type="error",
            conta_destino_info=None
        )
    
    
    resultado = confirmarTransferencia(conta_usuario, conta_destino, valor)

    if resultado["success"]:
        return redirect(url_for("transfer.transfer"))
    else:
        return render_template(
            "transfer/index.html",
            nome_usuario=session['user_info']['user_name'],
            conta_usuario=conta_usuario,
            conta_destino_info=conta_destino,
            popup_message=resultado["message"],
            popup_type="error"
        )