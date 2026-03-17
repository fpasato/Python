from flask import Blueprint, request, session, render_template
from flask import redirect, url_for
from utils.validators import get_account_by_id, get_account_by_number
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
        
        # Se for busca de conta
        if acao == "buscar":
            conta_destino_num = request.form.get("conta-destino")
            conta = get_account_by_number(conta_destino_num)
            
            if not conta:
                return render_template(
                    "transfer/index.html",
                    nome_usuario=session['user_info']['user_name'],
                    conta_usuario=conta_usuario, 
                    popup_message="Conta destino não encontrada",
                    popup_type="error",
                    conta_destino_info=None
                )
            
            conta_destino_info = {
                "nome": conta['nome_completo'],
                "numero_conta": conta['numero_conta'],
                "agencia": "0010",
                "saldo": conta['saldo']  
            }
            
            if conta_destino_num == conta_usuario['numero_conta']:
                return render_template(
                    "transfer/index.html",
                    nome_usuario=session['user_info']['user_name'],
                    conta_usuario=conta_usuario, 
                    popup_message="Não é possível transferir para a própria conta",
                    popup_type="error",
                    conta_destino_info=None
                )
                
            return render_template(
                "transfer/index.html",
                nome_usuario=session['user_info']['user_name'],
                conta_usuario=conta_usuario, 
                conta_destino_info=conta_destino_info
            )
        
        # Se for transferência direta (com valor)
        valor = request.form.get("valor")
        if valor:
            conta_destino_num = request.form.get("conta-destino")
            conta = get_account_by_number(conta_destino_num)
            
            if not conta:
                return render_template(
                    "transfer/index.html",
                    conta_usuario=conta_usuario, 
                    popup_message="Conta destino não encontrada",
                    popup_type="error",
                    conta_destino_info=None
                )
            
            conta_destino_info = {
                "nome": conta['nome_completo'],
                "numero_conta": conta['numero_conta'],
                "agencia": "0010",
                "saldo": conta['saldo']  
            }
            
            resultado = confirmarTransferencia(conta_usuario, conta_destino_info, float(valor))
            if resultado["success"]:
                return render_template(
                    "transfer/index.html",
                    nome_usuario=session['user_name'],
                    conta_usuario=conta_usuario, 
                    conta_destino_info=conta_destino_info, 
                    popup_message=resultado["message"],
                    popup_type="success"
                )
            else:
                return render_template(
                    "transfer/index.html",
                    nome_usuario=session['user_name'],
                    conta_usuario=conta_usuario, 
                    conta_destino_info=conta_destino_info, 
                    popup_message=resultado["message"],
                    popup_type="error"
                )
        
        # Default: mostrar formulário de busca
        return render_template(
            "transfer/index.html",
            nome_usuario=session['user_name'],
            conta_usuario=conta_usuario, 
            conta_destino_info=None
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
            nome_usuario=session['user_name'],
            conta_usuario=conta_usuario, 
            popup_message="Conta destino não encontrada",
            popup_type="error",
            conta_destino_info=None
        )
    
    conta_destino_info = {
        "nome": conta_destino['nome_completo'],
        "numero_conta": conta_destino['numero_conta'],
        "agencia": "0010",
        "saldo": conta_destino['saldo']
    }
    
   
    
    resultado = confirmarTransferencia(conta_usuario, conta_destino_info, valor)
    
    if resultado["success"]:
        return redirect(url_for("transfer.transfer"))
    else:
        return render_template(
            "transfer/index.html",
            nome_usuario=session['user_name'],
            conta_usuario=conta_usuario, 
            conta_destino_info=conta_destino_info, 
            popup_message=resultado["message"],
            popup_type="error"
        )