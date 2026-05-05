
class Processador:
    def __init__(self, modelo):
        self.modelo = modelo
     
    
class Memoria:
    def __init__(self, tamanho_gb):
        self.tamanho_gb = tamanho_gb
     

class Disco:
    def __init__(self, tipo, tamanho_gb):
        self.tipo = tipo
        self.tamanho_gb = tamanho_gb
        

class PlacaDeVideo:
    def __init__(self, modelo, vram_gb):
        self.modelo = modelo
        self.vram_gb = vram_gb


class Computador:
    def __init__(self, processador, memoria):
        self.processador = Processador(processador)
        self.memoria = Memoria(memoria)
        self.discos = []
        self.gpu = None      
  
    def mostrar_config(self):
        print(f'\nProcessador: {self.processador.modelo}')
        print(f'Memória RAM: {self.memoria.tamanho_gb}GB')
        for disco in self.discos:
            print(f'- {disco.tipo} {disco.tamanho_gb}GB')
        if self.gpu:
            print(f'GPU: {self.gpu.modelo}, {self.gpu.vram_gb}GB\n')

    def adicionar_gpu(self, gpu, vram_gb):
        if self.gpu:
            print('O computador já possui uma GPU!')
            return
        self.gpu = PlacaDeVideo(gpu, vram_gb)
        
    def remover_gpu(self):
        self.gpu = None
        
            
    def adicionar_disco(self, tipo, tamanho_gb):
        novo_disco = Disco(tipo, tamanho_gb) 
        self.discos.append(novo_disco)
        
    def upgrade_memoria(self, novo_tamanho):
        self.memoria.tamanho_gb =  novo_tamanho
        
    
            
c1 = Computador('Ryzen 5 5600', 16)

c1.adicionar_disco('SSD', 100)
c1.adicionar_gpu('RX 6750XT', 12)
c1.upgrade_memoria(32)

c1.mostrar_config()

c1.remover_gpu()
c1.adicionar_disco('HDD', 256)


c1.mostrar_config()


# Processador: Ryzen 5 5600
# Memória RAM: 32GB
# - SSD 100GB
# GPU: RX 6750XT, 12GB


# Processador: Ryzen 5 5600
# Memória RAM: 32GB
# - SSD 100GB
# - HDD 256GB