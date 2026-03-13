from nicegui import ui, app

# Import CSS
ui.add_css(open('components/Footer/component.css').read(), shared=True)

def footer():
    with ui.footer().classes('footer'):
        ui.label("Feito com ❤️ por Fer").classes('footer-text') 