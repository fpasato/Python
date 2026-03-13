from nicegui import ui

ui.add_css(open('components/InputArea/component.css').read(), shared=True)

def input_area(label, password=False):
    with ui.card().classes('input-container').props('flat bordered=false'):
        ui.label(label).classes('input-label')
        return ui.input(password=password).props('borderless').classes('input-field')
 