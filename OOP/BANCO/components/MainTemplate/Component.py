from nicegui import ui

ui.add_css(open('components/MainTemplate/component.css').read(), shared=True)

def main_template(content):

    # Header
    with ui.header().classes('main-header'):
        ui.image('/assets/logo.png') \
            .classes('logo') \
            .on('click', lambda: ui.navigate.to('/'))

    # Conteúdo da página
    with ui.column().classes('main-container'):
        content()

    # Footer
    with ui.footer().classes('main-footer'):
        ui.label('© 2026  - Meu Sistema')   