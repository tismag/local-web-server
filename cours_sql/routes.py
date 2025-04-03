from flask import Blueprint, render_template
import sqlite3

# Créer un blueprint pour les cours et SQL
cours_sql_bp = Blueprint('cours_sql', __name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@cours_sql_bp.route('/')
def index():
    conn = get_db_connection()
    courses = conn.execute('SELECT * FROM cours').fetchall()
    conn.close()
    return render_template('index.html', courses=courses)

@cours_sql_bp.route('/cours/<int:cours_id>')
def cours(cours_id):
    conn = get_db_connection()
    cours = conn.execute('SELECT * FROM cours WHERE id = ?', (cours_id,)).fetchone()
    students = conn.execute('''
        SELECT e.nom, e.prenom
        FROM etudiants e
        JOIN inscriptions i ON e.id = i.etudiant_id
        WHERE i.cours_id = ?
    ''', (cours_id,)).fetchall()
    conn.close()
    return render_template('cours.html', cours=cours, students=students)