# import sqlite3

# conn = sqlite3.connect("database.db")
# cursor = conn.cursor()

# cursor.execute("PRAGMA foreign_keys = OFF")

# tabelas = [
#     "transacoes_pix",
#     "transacoes_cartao",
#     "transacoes_conta",
#     "cartoes",
#     "chaves_pix",
#     "historico_precos",
#     "contas",
#     "usuarios"
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









import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

conta_id = 1  # usa um ID que existe

faturas_mensais = [
    ("luz", 120.50, "pendente", datetime.now() + timedelta(minutes=1), "Conta de luz"),
    ("agua", 80.30, "pendente", datetime.now() + timedelta(minutes=2), "Conta de água"),
    ("internet", 99.90, "pendente", datetime.now() + timedelta(minutes=3), "Internet"),
    ("aluguel", 500.00, "pendente", datetime.now() - timedelta(minutes=1), "Aluguel (vencido)"),
    ("celular", 59.90, "pendente", datetime.now() + timedelta(minutes=4), "Plano de celular"),
    ("academia", 89.90, "pendente", datetime.now() + timedelta(minutes=6), "Mensalidade academia"),
    ("streaming", 27.90, "pendente", datetime.now() + timedelta(minutes=7), "Assinatura streaming"),
]

tipos_aleatorios = [
    ("uber", "Corrida de aplicativo"),
    ("ifood", "Pedido delivery"),
    ("farmacia", "Compra na farmácia"),
    ("mercado", "Supermercado"),
    ("gasolina", "Abastecimento"),
    ("manutencao", "Conserto emergencial"),
    ("multa", "Multa de trânsito"),
    ("consulta", "Consulta médica"),
]

faturas_aleatorias = []

for tipo, descricao in tipos_aleatorios:
    valor = gerar_valor(tipo)
    
    faturas_aleatorias.append((
        tipo,
        valor,
        "pendente",
        datetime.now() + timedelta(minutes=random.randint(-5, 10)),
        descricao
    ))

cursor.executemany("""
    INSERT INTO faturas (conta_id, tipo, valor, status, data_vencimento, descricao)
    VALUES (?, ?, ?, ?, ?, ?)
""", [(conta_id, t, v, s, d.isoformat(), desc) for t, v, s, d, desc in faturas_mensais])

cursor.executemany("""
    INSERT INTO faturas (conta_id, tipo, valor, status, data_vencimento, descricao)
    VALUES (?, ?, ?, ?, ?, ?)
""", [(conta_id, t, v, s, d.isoformat(), desc) for t, v, s, d, desc in faturas_aleatorias])

conn.commit()
conn.close()

print("Faturas de teste criadas 🚀")