import sqlite3
 
conn = sqlite3.connect('database/Laboratorio.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Tarea (
                id INTEGER PRIMARY KEY,
                contenido TEXT,
                estado INTEGER
             )''')
conn.commit()
 