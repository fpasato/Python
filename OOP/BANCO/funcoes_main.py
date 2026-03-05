import tkinter as tk

def apenas_numeros(valor):
    return valor.isdigit() or valor == ""

def entrar(cpf, frame_cliente, frame_login):
    try:
        # Valida se CPF está vazio
        if not cpf or cpf.strip() == "":
            tk.Label(frame_login, text="CPF não pode estar vazio!", 
                    bg="azure", fg="red").pack(pady=5)
            frame_login.pack(fill="both", expand=True)
            return
            
        from banco import verifica_cliente
        import json
        import os
        
        if verifica_cliente(cpf):
            # Carrega os dados do cliente
            caminho_json = os.path.join(os.path.dirname(__file__), "contas.json")
            with open(caminho_json) as f:
                clientes = json.load(f)
            
            # Esconde login e mostra cliente
            frame_login.pack_forget()
            from templates.LoginTemplate.login import criar_frame_cliente
            criar_frame_cliente(frame_cliente, cpf, frame_login, clientes)
        else:
            # Mostra erro e garante que login está visível
            tk.Label(frame_login, text="Cliente não encontrado!", 
                    bg="azure", fg="red").pack(pady=5)
            frame_login.pack(fill="both", expand=True)  
        
    except Exception as e:
        tk.Label(frame_login, text=f"Erro: {str(e)}", 
                bg="azure", fg="red").pack(pady=5)
        frame_login.pack(fill="both", expand=True) 