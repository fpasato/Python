import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# cursor.execute("PRAGMA foreign_keys = OFF")

# tabelas = [
#     "transacoes_pix",
#     "transacoes_cartao",
#     "transacoes_conta",
#     "cartoes",
#     "chaves_pix",
#     "historico_precos",
#     "contas",
#     "usuarios",
#     "faturas"
# ]

# for tabela in tabelas:
#     cursor.execute(f"DELETE FROM {tabela}")

# # reset autoincrement
# cursor.execute("DELETE FROM sqlite_sequence")

# # adicionar salario se não existir
# cursor.execute("PRAGMA table_info(contas)")
# colunas = [col[1] for col in cursor.fetchall()]

# if "salario" not in colunas:
#     cursor.execute("""
#         ALTER TABLE contas
#         ADD COLUMN salario INTEGER DEFAULT 1518
#     """)

# cursor.execute("PRAGMA foreign_keys = ON")

# conn.commit()
# conn.close()

# print("✅ Banco limpo e atualizado (investimentos preservados).")







cursor.execute("DELETE FROM investimentos_temporarios")

conn.commit()
conn.close()

print("Banco criado com sucesso 🚀")