from nicegui import ui
from components.Container.Container import container
from components.SectionTemplate.Component import section_template
from components.ButtonPattern.Component import button_pattern
from pages.withdraw_page.withdraw import withdraw_page

ui.add_css(open('pages/dashboard_page/dashboard.css').read(), shared=True)

def dashboard_page():
    with container():
        with ui.element('div').classes('divdashboard'):
            ui.label('Bem vindo ao Banco').classes('text-2xl font-bold')
            with section_template():
                button_pattern('Sacar').on('click', lambda: ui.navigate.to('/withdraw'))
                button_pattern('Depositar')
                button_pattern('Transferir')
                button_pattern('Ver Extrato')
                button_pattern('Ver Saldo') 
                button_pattern('Investir')