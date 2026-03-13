from nicegui import ui

ui.add_css(open('components/ButtonPattern/component.css').read(), shared=True)

def button_pattern(text):
    btn = ui.element('button').classes('button-pattern')
    ui.label(text).classes('button-pattern-text') 
    return btn