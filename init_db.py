import sqlite3

connection = sqlite3.connect('inventory.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO inv (suz,client,service,pe,pe_if,vid) VALUES (?, ?, ?, ?, ?, ?)",
            ('СУЗ-00000', 'ТЕСТОВЫЙ КЛИЕНТ', 0, '10.1.1.1', 'ge-0/0/0', '4096')
            )

connection.commit()
connection.close()
