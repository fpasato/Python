from flask import Blueprint, render_template, request, session, redirect
from utils.services.banco.emprestimo import simularEmprestimo


emprestimos_bp = Blueprint("emprestimos", __name__, url_prefix="/emprestimos")


@emprestimos_bp.route("/")
def emprestimos():
    if 'user_id' not in session:
        return redirect("/login")
    
    if request.method == "POST":
        valor = request.form.get("valor", type=float)
        parcelas = request.form.get("parcelas", type=int)
    else:
        valor = request.args.get("valor", type=float)
        parcelas = request.args.get("parcelas", type=int)
        
    resultado = None
    if valor and parcelas:
        resultado = simularEmprestimo(valor, parcelas)
    
    print(resultado)
    
    if valor and parcelas:
        return render_template("emprestimos/index.html", resultado=resultado)
    
    return render_template("emprestimos/index.html")
