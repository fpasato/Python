from nicegui import ui
from services.auth_service import login
from components.InputArea.Component import input_area
from components.ButtonPattern.Component import button_pattern

ui.add_css(open('components/LoginSection/login.css').read(), shared=True)

def login_section():
    with ui.card().classes('login-card'):
        with ui.row().classes('logo-row'):
            ui.image('assets/avatar.svg').classes('login-icon')
        cpf = input_area('CPF: ')
        senha = input_area('Senha:', password=True) 
    
        def fazer_login(): 
            usuario = login(cpf.value, senha.value)
            if usuario: 
                ui.navigate.to('/dashboard')
 
        # "div" para os botões
        with ui.row().classes('buttons-row'):
            button_pattern('Entrar').on('click', fazer_login)
            button_pattern('Cadastrar') 