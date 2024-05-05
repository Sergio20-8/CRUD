import sqlite3
from flask import Flask, render_template, request, g, redirect, url_for

app = Flask(__name__)
app.config['DATABASE'] = 'database/Laboratorio.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    conn = get_db()
    cursor = conn.execute('SELECT id, contenido, estado FROM Tarea WHERE estado = 1')
    tareas = cursor.fetchall()
    return render_template('index.html', tareas=tareas)

@app.route('/crear-tarea', methods=['POST'])
def crear():
    conn = get_db()
    tarea_data = (request.form['content'], 1)

    conn.execute('INSERT INTO Tarea (contenido, estado) VALUES (?, ?)', tarea_data)
    conn.commit()
    return redirect(url_for('home'))


@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    conn = get_db()
    conn.execute('UPDATE Tarea SET estado = 0 WHERE id = ?', (id,))
    conn.commit()
    return redirect(url_for('home'))


@app.route('/actualizar-tarea/<id>')
def actualizar(id):
    conn = get_db()
    tarea = conn.execute('SELECT id, contenido FROM Tarea WHERE id = ?', (id,)).fetchone()
   
    return render_template('actualizar.html', tarea=tarea)

@app.route('/actualizar-tarea/<int:id>', methods=['POST'])
def guardar_cambios(id):
    conn = get_db()
    if request.method == 'POST':
        nuevo_contenido = request.form['nuevo_contenido']
        conn.execute('UPDATE Tarea SET contenido = ? WHERE id = ?', (nuevo_contenido, id))
        conn.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
