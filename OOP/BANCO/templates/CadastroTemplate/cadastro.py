import tkinter as tk

from banco import Banco

def cadastro(frame_cadastro, cpf_entry_widget, btn_entrar_widget, btn_cadastrar_widget):
    """Cria a interface do frame de cadastro de cliente"""
    
    # Esconder widgets do login
    cpf_entry_widget.pack_forget()
    btn_entrar_widget.pack_forget()
    btn_cadastrar_widget.pack_forget()
    
    label = tk.Label(frame_cadastro, text="Cadastro de Cliente")
    label.pack(padx=20, pady=10)
    
    label_nome = tk.Label(frame_cadastro, text="Nome:")
    label_nome.pack(padx=20, pady=5)
    
    entry_nome = tk.Entry(frame_cadastro)
    entry_nome.pack(padx=20, pady=5)
    
    label_cpf = tk.Label(frame_cadastro, text="CPF:")
    label_cpf.pack(padx=20, pady=5)
    
    entry_cpf = tk.Entry(frame_cadastro)
    entry_cpf.pack(padx=20, pady=5)
    
    button_cadastrar = tk.Button(frame_cadastro, text="Cadastrar")
    button_cadastrar.config(command=lambda: Banco.cadastrar_cliente(entry_nome.get(), entry_cpf.get()))
    button_cadastrar.pack(padx=20, pady=10)
    
    button_voltar = tk.Button(frame_cadastro, text="Voltar")
    button_voltar.config(command=lambda: voltar_login(frame_cadastro, cpf_entry_widget, btn_entrar_widget, btn_cadastrar_widget))
    button_voltar.pack(padx=20, pady=10)

def voltar_login(frame_cadastro, cpf_entry_widget, btn_entrar_widget, btn_cadastrar_widget):
    """Volta para a tela de login e mostra os widgets escondidos"""
    # Limpa apenas os widgets do cadastro (não destrói, apenas remove do frame)
    for widget in frame_cadastro.winfo_children():
        widget.pack_forget()
    
    # Mostra novamente os widgets do login
    cpf_entry_widget.pack(padx=20, pady=10)
    btn_entrar_widget.pack(padx=20, pady=10)
    btn_cadastrar_widget.pack(padx=20, pady=10)

