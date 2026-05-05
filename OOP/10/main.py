
from pathlib import Path
from abc import ABC, abstractmethod

LOG_FILE = Path(__file__).parent / 'log.txt'


class Log(ABC):
    
    @abstractmethod
    def _log(self, msg):...
        

    def log_error(self, msg):
        return self._log(f'Error: {msg}')        

    def log_success(self, msg):
        return self._log(f'Success: {msg}')      
    
      
class LogFileMixin(Log):
    
    def _log(self, msg):
        msg_formatada = f'{msg} {self.__class__.__name__}'
        print(f'Salvando no log:{msg_formatada}')
        with open(LOG_FILE, 'a') as arquivo:
            arquivo.write(msg_formatada)
            arquivo.write('\n')
        
        
class LogPrintMixin(Log):
    
    def _log(self, msg):
        print(f"{msg} {self.__class__.__name__}")
    



lp = LogPrintMixin()
lp.log_error("Deu errado")
lp.log_success('Deu certo')

# lf =  LogFileMixin()
# lf.log_error('Algo deu errado')
# lf.log_success('Que legal ') 

        
        