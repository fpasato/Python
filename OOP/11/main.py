# Exercício: Sistema de Pagamentos
# Você vai criar um sistema onde existem diferentes formas de pagamento.
# Objetivo (o coração da abstração)
# Você deve criar uma classe base abstrata que define o comportamento comum, 
# mas não implementa tudo.

from abc import ABC, abstractmethod
import time

class Pagamento(ABC):
    
    def __init__(self, valor):
      self._valor = valor
    
    @abstractmethod
    def calcular_valor(self):
        pass
        
    @abstractmethod
    def get_tipo_pagamento(self):
        pass
        
    def pagar(self):
        valor_total = self.calcular_valor()
        print()
        print(f"Pagando R${valor_total:.2f} com {self.get_tipo_pagamento()}")
        time.sleep(2)
        print("Pagamento confirmado!")
        
    
    
class CartaoCredito(Pagamento):
    def __init__(self, valor):
        super().__init__(valor)
    
    def calcular_valor(self):
        # 5 % de taxa
        return self._valor * 1.05
        
    def get_tipo_pagamento(self):
        return "cartão de crédito"
       
       
class Boleto(Pagamento):
    def __init__(self, valor):
        super().__init__(valor)
    
    def calcular_valor(self):
        return self._valor * 0.9
        
    def get_tipo_pagamento(self):
        return "boleto"
        
class Pix(Pagamento):
    def __init__(self, valor):
        super().__init__(valor)
    
    def calcular_valor(self):
        return self._valor
        
    def get_tipo_pagamento(self):
        return "pix"
        
        
pagamentos = [
    CartaoCredito(100),
    Boleto(100),
    Pix(100)
]

for p in pagamentos:
    p.pagar()