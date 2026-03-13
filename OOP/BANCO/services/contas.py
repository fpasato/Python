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

    @staticmethod
    def verifica_monetario(valor):

        if not isinstance(valor, (int, float)):
            raise TypeError("Valor deve ser numérico")

        if valor <= 0:
            raise ValueError("Valor deve ser positivo")

    def depositar(self, valor):

        self.verifica_monetario(valor)

        self._saldo += valor
        self.historico.append(f"{datetime.now()} - Depósito")

    def sacar(self, valor):

        self.verifica_monetario(valor)

        if valor <= self._saldo:

            self._saldo -= valor
            self.historico.append(f"{datetime.now()} - Saque")

            return True

        return False

class ContaCorrente(Conta):

    def __init__(self, titular, cpf):
        super().__init__(titular, cpf)
        self.limite_extra = 1000

    def sacar(self, valor_saque):

        self.verifica_monetario(valor_saque)

        if valor_saque <= self._saldo + self.limite_extra:

            self._saldo -= valor_saque

            self.historico.append(
                f"{datetime.now()} - Saque realizado"
            )

            return True

        print("Valor do saque excede limite")
        return False
    

class ContaPoupanca(Conta):
    def __init__(self, titular, cpf):
        super().__init__(titular, cpf)
        
    def render_juros(self):
        fator_juros = random.uniform(1.05, 1.1)
        self._saldo *= fator_juros
        self.historico.append(f"{datetime.now()} - Juros aplicados")
        return self._saldo
 

