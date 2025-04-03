import sqlite3

def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Création des tables
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS cours (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        description TEXT,
        duree INTEGER
    );

    CREATE TABLE IF NOT EXISTS professeurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS etudiants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS inscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        etudiant_id INTEGER,
        cours_id INTEGER,
        FOREIGN KEY (etudiant_id) REFERENCES etudiants(id),
        FOREIGN KEY (cours_id) REFERENCES cours(id)
    );

    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        etudiant_id INTEGER,
        cours_id INTEGER,
        note FLOAT CHECK (note >= 0 AND note <= 20),
        commentaire TEXT,
        FOREIGN KEY (etudiant_id) REFERENCES etudiants(id),
        FOREIGN KEY (cours_id) REFERENCES cours(id)
    );
    ''')
    
    conn.commit()
    conn.close()
    print("Base de données créée avec succès.")

if __name__ == "__main__":
    create_database()
