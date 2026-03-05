
import json
from contas import ContaCorrente, ContaPoupanca
import uuid
import os

class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.contas = []


class Banco:
    def __init__(self):
        caminho_json = os.path.join(os.path.dirname(__file__), "contas.json")
        with open(caminho_json) as f:
            self.clientes = json.load(f)

    def cadastrar_cliente(self, cliente, tipo):
        # 1. Verifica se cliente existe
        if cliente.cpf not in self.clientes:
            # Criar cliente novo
            self.clientes[cliente.cpf] = {
                "titular": cliente.nome,
                "contas": []
            }
            
        # Verifica se já tem conta do tipo
        contas_cliente = self.clientes[cliente.cpf]["contas"]
        if any(c["tipo"] == tipo for c in contas_cliente): 
            print("Cliente já possui uma conta " + tipo)
            return
        
        # Criar conta e adicionar
        nova_conta = {
            "tipo": tipo,
            "id": (tipo[:2]).upper() + str(uuid.uuid4())[:12],
            "saldo": 0,
            "limite_extra": 1000 if tipo == "corrente" else 0
        }
        
        contas_cliente.append(nova_conta)
        
        # Salva
        cliente.contas.append(nova_conta)
        with open('contas.json', 'w') as f:
            json.dump(self.clientes, f)

        return nova_conta
        
    def sacar(self, cpf, tipo_conta, valor):
        if not verica_cliente(cpf):
            return
        
        contas_cliente = self.clientes[cpf]["contas"]
        
        for conta in contas_cliente:
            if conta["tipo"] == tipo_conta:
                if tipo_conta == "corrente":
                    conta_corrente = ContaCorrente(cliente.nome, cliente.cpf)
                    conta_corrente.sacar(valor)
                elif tipo_conta == "poupanca":
                    conta_poupanca = ContaPoupanca(cliente.nome, cliente.cpf)
                    conta_poupanca.sacar(valor)
        print("Conta não encontrada")
        return
        
    def depositar(self, cpf, valor, tipo_conta):
        if not verica_cliente(cpf):
            return
        
        contas_cliente = self.clientes[cpf]["contas"]
        
        for conta in contas_cliente:
            if conta["tipo"] == tipo_conta:
                conta["saldo"] += valor
                print("Deposito realizado com sucesso")
                with open('contas.json', 'w') as f:
                    json.dump(self.clientes, f)
                return
        print("Conta não encontrada")
        return 

    def consulta_saldo(self, cpf, tipo_conta):
        if not verica_cliente(cpf):
            return
        
        contas_cliente = self.clientes[cpf]["contas"]
        
        for conta in contas_cliente:
            if conta["tipo"] == tipo_conta:
                print(f"Saldo: {conta['saldo']}")
                return
        print("Conta não encontrada")
        return

def verifica_cliente(cpf):
    try:
        caminho_json = os.path.join(os.path.dirname(__file__), "contas.json")
        with open(caminho_json) as f:
            clientes = json.load(f)
        
        if cpf not in clientes:
            print("Cliente não encontrado")
            return False
        return True
    
    except Exception as e:
        print(f"Erro ao verificar cliente: {e}")
        return False











