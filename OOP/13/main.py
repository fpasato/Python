
from abc import ABC, abstractmethod

class Notificacao(ABC):
    def __init__(self, mensagem) -> None:
        self.mensagem = mensagem
        
        
    @abstractmethod   
    def enviar(self) -> bool:
        pass        
        
        
class NotificacaoEmail(Notificacao):
    def enviar(self):
        print('E-mail: enviando:', self.mensagem)        
        return True
        
class NotificacaoSMS(Notificacao):
    def enviar(self):
        print('SMS: enviando:', self.mensagem)
        return False
        

def  notifica(notificacao: Notificacao):
    notificacao_enviada = notificacao.enviar()
    
    if notificacao_enviada:
        print('Notificação enviada')
    else:
        print('Notificação NÂO enviada')
        

notifica_email = notifica(NotificacaoEmail("Testando EMAIL"))
notifica_SMS = notifica(NotificacaoSMS("Testando SMS"))