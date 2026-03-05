import tkinter as tk

def login(frame_login):
    """Cria a interface do frame do cliente"""
    # Limpa frame anterior
    for widget in frame_login.winfo_children():
        widget.destroy()
    
    # Configura o grid para expandir
    frame_cliente.grid_rowconfigure(0, weight=1)
    frame_cliente.grid_columnconfigure(0, weight=1)
    
    # Frame central para melhor organização
    frame_central = tk.Frame(frame_cliente, bg="azure")
    frame_central.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    # Cria interface do cliente com grid
    tk.Label(frame_central, text=f"Bem-vindo, {clientes[cpf]['titular']}", 
            bg="azure", fg="black", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
    
    tk.Button(frame_central, text="Ver Saldo", width=15).grid(row=1, column=0, padx=10, pady=5)
    tk.Button(frame_central, text="Sacar", width=15).grid(row=1, column=1, padx=10, pady=5)
    
    tk.Button(frame_central, text="Depositar", width=15).grid(row=2, column=0, padx=10, pady=5)
    tk.Button(frame_central, text="Transferir", width=15).grid(row=2, column=1, padx=10, pady=5)
    
    tk.Button(frame_central, text="Extrato", width=15).grid(row=3, column=0, padx=10, pady=5)
    tk.Button(frame_central, text="Histórico", width=15).grid(row=3, column=1, padx=10, pady=5)
    
    tk.Button(frame_central, text="Sair", width=15, bg="red", fg="white",
             command=lambda: voltar_login(frame_cliente, frame_login)).grid(row=4, column=0, columnspan=2, pady=20)



def voltar_login(frame_cliente, frame_login):
    """Volta para a tela de login e limpa mensagens de erro"""
    frame_cliente.pack_forget()
    
    # Limpa apenas labels de erro (cor vermelha)
    widgets_para_remover = []
    for widget in frame_login.winfo_children():
        if isinstance(widget, tk.Label) and widget.cget("fg") == "red":
            widgets_para_remover.append(widget)
    
    for widget in widgets_para_remover:
        widget.destroy()
    
    # Limpa campo CPF
    for widget in frame_login.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
            break
    frame_login.pack(fill="both", expand=True)