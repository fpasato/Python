
from nicegui import ui
from contextlib import contextmanager

ui.add_css(open('components/Container/Container.css').read(), shared=True)

@contextmanager  
def container():
    with ui.card().classes('menu-container'):
        yield   