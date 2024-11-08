from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Database configuration
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# Create a database if it doesn't exist
def create_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY, title TEXT, content TEXT)''')
    conn.commit()
    conn.close()

create_db()

@app.route('/')
def index():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    c = conn.cursor()
    c.execute('SELECT id, title FROM notes')
    notes = c.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    c = conn.cursor()
    c.execute('INSERT INTO notes (title, content) VALUES (%s, %s)', (title, content))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/view_note/<int:note_id>')
def view_note(note_id):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    c = conn.cursor()
    c.execute('SELECT title, content FROM notes WHERE id = %s', (note_id,))
    note = c.fetchone()
    conn.close()
    return render_template('view_note.html', note=note)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
