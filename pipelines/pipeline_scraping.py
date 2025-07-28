# pipelines/pipeline_scraping.py

import os
from get_data.get_scraping_data import scrape_books
from process_data.process_scrapping_data import clean_book_data
from database.insert_data import create_connection, create_table, insert_books

DATA_PATH = "data/data_scraping.csv"


def run_scraping_pipeline(pages: int = 1):
    print("Étape 1 : Scraping des livres...")
    df_raw = scrape_books(pages)

    if df_raw.empty:
        print("Aucun livre récupéré. Fin du pipeline.")
        return

    print("Étape 2 : Sauvegarde des données brutes dans data/data_scraping.csv...")
    os.makedirs("data", exist_ok=True)
    df_raw.to_csv(DATA_PATH, index=False)
    print(f"{len(df_raw)} livres sauvegardés.")

    print("Étape 3 : Nettoyage et transformation des données...")
    df_clean = clean_book_data(df_raw)

    print("Étape 4 : Insertion des données en base...")
    conn = create_connection()
    if conn:
        create_table(conn)
        insert_books(conn, df_clean)
        conn.close()

    print("Pipeline terminé avec succès ")
