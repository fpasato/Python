import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()



cursor.execute("DELETE FROM investimentos_temporarios WHERE duracao > 3600000;")
cursor.execute("DELETE FROM investimentos_temporarios WHERE duracao <= 0 OR duracao > 86400000;")

conn.commit()
conn.close()
