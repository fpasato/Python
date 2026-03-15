

from flask import Blueprint, request, session, render_template
from utils.validators import get_account_by_id, get_account_by_number

transfer_bp = Blueprint("transfer", __name__, url_prefix="/transfer")

@transfer_bp.route("/", methods=["GET", "POST"])
def transfer():
    contausuario = get_account_by_id(session['user_id'])
    if request.method == "GET":
        return render_template(
            "transfer/index.html",
            nome_usuario=session['user_name'],
            contausuario=contausuario,  
            conta_destino_info=None
        )

    elif request.method == "POST":
        conta_destino_num = request.form.get("conta-destino")
        conta = get_account_by_number(conta_destino_num)
        
        if not conta:
            return render_template(
                "transfer/index.html",
                nome_usuario=session['user_name'],
                contausuario=contausuario,  # ✅ passa aqui também
                popup_message="Conta destino não encontrada",
                popup_type="error",
                conta_destino_info=None
            )
        
        conta_destino_info = {
            "nome": conta['nome_completo'],
            "numero_conta": conta['numero_conta'],
            "agencia": "0010",
            "saldo": "0.00"
        }
        
        return render_template(
            "transfer/index.html",
            nome_usuario=session['user_name'],
            contausuario=contausuario, 
            conta_destino_info=conta_destino_info, 
            debug_var="TESTE"
        )
    