
from  flask import Blueprint

extrato_bp = Blueprint('extrato', __name__, url_prefix='/extrato')

@extrato_bp.route('/extrato')
def extrato():
    pass