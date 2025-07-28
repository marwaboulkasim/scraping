# database/insert_data.py

import sqlite3
import pandas as pd


def create_connection(db_file="books.db"):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base : {e}")
        return None


def create_table(conn):
    create_sql = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price REAL,
        availability INTEGER,
        rating INTEGER
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_sql)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur création table : {e}")


def insert_books(conn, df: pd.DataFrame):
    try:
        df.to_sql("books", conn, if_exists="append", index=False)
        print(f"{len(df)} livres insérés dans la base.")
    except sqlite3.Error as e:
        print(f"Erreur insertion : {e}")
