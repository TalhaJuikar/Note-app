from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create a database if it doesn't exist
def create_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)''')
    conn.commit()
    conn.close()

create_db()

@app.route('/')
def index():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    notes = c.execute('SELECT id, title FROM notes').fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (title, content))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/view_note/<int:note_id>')
def view_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    note = c.execute('SELECT title, content FROM notes WHERE id = ?', (note_id,)).fetchone()
    conn.close()
    return render_template('view_note.html', note=note)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
