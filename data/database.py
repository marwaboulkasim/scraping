# data/database.py
import sqlite3
import pandas as pd

DB_NAME = "books.db"

def create_connection(db_name: str = DB_NAME):
    """Créer une connexion à la base SQLite."""
    try:
        conn = sqlite3.connect(db_name)
        print(f"Connexion à la base {db_name} réussie.")
        return conn
    except sqlite3.Error as e:
        print(f"Erreur de connexion : {e}")
        return None

def create_table(conn):
    """Créer la table books si elle n'existe pas."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price REAL,
        rating REAL,
        availability INTEGER
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur création table : {e}")

def insert_books_to_db(df: pd.DataFrame, conn):
    """Insérer les livres du DataFrame dans la base."""
    create_table(conn)  # On s'assure que la table existe
    try:
        df.to_sql("books", conn, if_exists="append", index=False)
        print(f"{len(df)} livres insérés dans la base.")
    except Exception as e:
        print(f"Erreur insertion données : {e}")

def count_books_in_db(conn):
    """Compter le nombre de livres dans la table."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM books;")
        count = cursor.fetchone()[0]
        print(f"Total livres en base : {count}")
        return count
    except sqlite3.Error as e:
        print(f"Erreur comptage : {e}")
        return 0

def close_connection(conn):
    """Fermer la connexion à la base."""
    if conn:
        conn.close()
        print("Connexion à la base fermée.")
