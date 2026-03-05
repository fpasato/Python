import uuid
import random
from datetime import datetime

class Conta:
    def __init__(self, titular, cpf):
        self.titular = titular
        self.cpf = cpf
        self._saldo = 0
        self.id = str(uuid.uuid4()) 
        self.historico = []
    
    def verifica_monetario(valor):
        if not isinstance(valor, (int, float)):
            raise TypeError("Valor deve ser numérico")
        if valor < 0:
            raise ValueError("Valor deve ser positivo")
        return True
        
    def depositar(conta, valor):
        verifica_monetario(valor)
        conta._saldo += valor
        conta.historico.append(f"{datetime.now()} - Depósito realizado")
        print("Depósito realizado com sucesso")
    
    def sacar(conta, valor):
        verifica_monetario(valor)
        if valor <= conta._saldo:
            conta._saldo -= valor
            conta.historico.append(f"{datetime.now()} - Saque realizado")
            print("Saque realizado com sucesso")
            return True
        else:
            print("Valor do saque excede saldo")
            return False
        
    @property
    def saldo(self):
        return round(self._saldo,2)


class ContaCorrente(Conta):
    def __init__(self, titular, cpf):
        super().__init__(titular, cpf)
        self.limite_extra = 1000
            
    def sacar(self, valor_saque):
        verifica_monetario(valor_saque)
        if valor_saque <= self._saldo + self.limite_extra:
            self._saldo -= valor_saque
            self.historico.append(f"{datetime.now()} - Saque realizado")
        else:
            print("Valor do saque excede limite")
            return False
         
        return True
    

class ContaPoupanca(Conta):
    def __init__(self, titular, cpf):
        super().__init__(titular, cpf)
        
    def render_juros(self):
        fator_juros = random.uniform(1.05, 1.1)
        self._saldo *= fator_juros
        self.historico.append(f"{datetime.now()} - Juros aplicados")
        return self._saldo
 

