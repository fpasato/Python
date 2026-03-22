import sqlite3
from utils.validators import get_db

conn = get_db()
try:
    # Verifica se a coluna já existe
    cursor = conn.execute('PRAGMA table_info(carteira_investimentos)')
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'vencimento' not in columns:
        conn.execute('ALTER TABLE carteira_investimentos ADD COLUMN vencimento DATETIME NULL')
        print('Campo vencimento adicionado com sucesso!')
    else:
        print('Campo vencimento já existe na tabela.')
        
    conn.commit()
except Exception as e:
    print(f'Erro: {e}')
finally:
    conn.close()
