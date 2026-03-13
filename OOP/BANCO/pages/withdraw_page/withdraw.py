from nicegui import ui
from components.MainTemplate.Component import main_template
from components.SectionTemplate.Component import section_template
from components.ButtonPattern.Component import button_pattern
from services.session import get_usuario_logado, salvar_dados
from services.banco import Banco

ui.add_css(open('pages/withdraw_page/withdraw.css').read(), shared=True)

#pagina de saque
def withdraw_page():
    main_template(withdraw)
    
def withdraw():
    usuario = get_usuario_logado()
    
    if not usuario:
        ui.label("Usuário não está logado").classes('text-red-500')
        return
    
    # Informações do titular
    with ui.card().classes('user-info-card mb-6'):
        ui.label('Informações do Titular').classes('text-lg font-bold mb-3 text-center')
        ui.label(f'Nome: {usuario.get("nome", "N/A")}').classes('mb-2')
        ui.label(f'CPF: {usuario.get("cpf", "N/A")}').classes('mb-4')
    
    # Lista de contas do usuário
    contas = usuario.get("contas", {})
    
    if not contas:
        ui.label("Usuário não possui contas").classes('text-red-500')
        return
    
    with ui.card().classes('accounts-card'):
        ui.label('Suas Contas').classes('text-lg font-bold mb-4 text-center')
        
        for conta_id, conta in contas.items():
            saldo = conta.get("saldo", 0)
            tipo = conta.get("tipo", "N/A")
            limite = conta.get("limite_extra", 0)
            
            with ui.card().classes('account-item'):
                with ui.row().classes('account-header'):
                    ui.label(f'Conta: {conta_id}').classes('font-bold')
                    ui.label(f'Tipo: {tipo.upper()}').classes('ml-auto')
                
                ui.label(f'Saldo: R${saldo:.2f}').classes('text-xl font-bold text-green-600 mb-2')
                
                if tipo == "corrente" and limite > 0:
                    ui.label(f'Limite Extra: R${limite:.2f}').classes('text-blue-600 mb-2')
                    ui.label(f'Disponível para saque: R${saldo + limite:.2f}').classes('text-sm text-gray-600')
    
    # Formulário de saque
    with ui.card().classes('withdraw-form-card mt-6'):
        ui.label('Realizar Saque').classes('text-lg font-bold mb-4 text-center')
        
        valor_input = ui.input('Valor do saque:', placeholder='0.00').classes('w-full mb-4')
        
        # Selecionar conta - apenas se houver contas
        contas_lista = list(contas.keys())
        
        # Botão para realizar saque
        def fazer_saque():
            try:
                valor = float(valor_input.value)
                
                if valor <= 0:
                    ui.notify('Valor deve ser maior que zero', type='negative')
                    return
                
                # Se não há contas, não permite saque
                if not contas_lista:
                    ui.notify('Nenhuma conta disponível para saque', type='negative')
                    return
                
                # Usar a função do Banco com a primeira conta
                banco = Banco()
                cpf_usuario = usuario.get('cpf')
                primeira_conta_id = contas_lista[0]
                primeira_conta = contas[primeira_conta_id]
                tipo_conta = primeira_conta["tipo"]
                
                # Tentar fazer o saque usando a classe Banco
                resultado = banco.sacar(cpf_usuario, tipo_conta, valor)
                
                if resultado:
                    # Atualizar dados do usuário com o novo saldo
                    # Ler dados atualizados do banco
                    contas_atualizadas = banco.clientes.get(cpf_usuario, {}).get("contas", {})
                    
                    # Encontrar a conta atualizada
                    for id_conta, conta_atualizada in contas_atualizadas.items():
                        if conta_atualizada.get("tipo") == tipo_conta:
                            # Atualizar o usuário na sessão
                            usuario["contas"][id_conta] = conta_atualizada
                            break
                    
                    ui.notify(f'Saque de R${valor:.2f} realizado com sucesso!', type='positive')
                    
                    # Salvar dados atualizados
                    salvar_dados()
                else:
                    ui.notify('Erro ao realizar saque', type='negative')
                
            except ValueError:
                ui.notify('Digite um valor válido', type='negative')
        
        # Botão apenas se houver contas
        if contas_lista:
           button_pattern('Confirmar Saque').on('click', fazer_saque)
        
        # Mensagem informativa se não houver contas
        if not contas_lista:
            ui.label('Nenhuma conta disponível para saque').classes('text-red-500 text-center mt-4')