from nicegui import ui

ui.add_css(open('components/SectionTemplate/component.css').read(), shared=True)

def section_template():
    return ui.card().classes('section-container')
        
   