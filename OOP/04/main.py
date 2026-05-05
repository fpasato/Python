

class Carro:
    def __init__(self, nome):
        self.nome = nome
        self.motor = None
        self.fabricante = None
        
class Motor:
    def __init__(self, nome):
        self.nome = nome
        
class Fabricante:
    def __init__(self, nome):
        self.nome = nome
        self.carros = []
        
    def fabrica_carros(self, nome, motor):
        novo_carro = Carro(nome)
        novo_carro.motor = motor
        novo_carro.fabricante= self
        
        self.carros.append(novo_carro)
        
        return novo_carro
    
    def lista_carros(self):
        for carro in self.carros:
            print(f'Modelo: {carro.nome}\nMotor: {carro.motor.nome}\nFabricante: {carro.fabricante.nome}')
        
        
mazda = Fabricante('mazda')
nissan = Fabricante('nissan')

v8 = Motor('v8')
Wankel = Motor('Wankel')

c1 = mazda.fabrica_carros('rx7', Wankel)
c2 = nissan.fabrica_carros('gtr r33', Wankel)

# print(c1.nome)
# print(c1.motor.nome)
# print(c1.fabricante.nome)
# print('#' * 20)

# print(c2.nome)
# print(c2.motor.nome)
# print(c2.fabricante.nome)


mazda.lista_carros()
print()
print()
print()
print()
nissan.lista_carros()
