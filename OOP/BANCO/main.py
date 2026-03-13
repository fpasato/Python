from nicegui import ui, app
from pages.login_page.login_page import login_page
from pages.dashboard_page.dashboard import dashboard_page
from pages.withdraw_page.withdraw import withdraw_page
from components.MainTemplate.Component import main_template



ui.add_css(open('styles/main.css').read(), shared=True)
app.add_static_files('/assets', 'assets')

@ui.page('/')
def home():
    main_template(login_page)
    

@ui.page('/dashboard')
def dashboard():
    main_template(dashboard_page)

@ui.page('/withdraw')
def withdraw():
    withdraw_page()

ui.run(
    host='127.0.0.1',
    port=10396,
    reload=True    
)