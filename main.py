"""
Script principal pour le scraping et traitement des données de livres
"""

import argparse
import sys
from scraper import scrape_books
from data.processor import create_dataframe_from_books, save_to_csv
from data.database import create_connection, insert_books_to_db, count_books_in_db, close_connection
from config.settings import DEFAULT_PAGES_TO_SCRAPE


def scrape_and_save(pages: int = DEFAULT_PAGES_TO_SCRAPE, save_csv: bool = True, save_db: bool = True) -> None:
    """Scrape books data and save to CSV and/or database."""
    print("=" * 50)
    print("DÉBUT DU SCRAPING")
    print("=" * 50)

    books_data = scrape_books(pages)

    if not books_data:
        print("Aucune donnée récupérée. Arrêt du programme.")
        return

    print("\nTraitement des données...")
    df_books = create_dataframe_from_books(books_data)

    print(f"\nRésumé des données:")
    print(f"- Total des livres: {len(df_books)}")
    print(f"- Livres disponibles: {df_books['availability'].sum()}")
    print(f"- Prix moyen: £{df_books['price'].mean():.2f}")
    print(f"- Note moyenne: {df_books['rating'].mean():.1f}/5")

    if save_csv:
        print("\nSauvegarde CSV...")
        save_to_csv(df_books)

    if save_db:
        print("\nSauvegarde en base de données...")
        connection = create_connection()
        if connection:
            insert_books_to_db(df_books, connection)
            count_books_in_db(connection)
            close_connection(connection)

    print("\n" + "=" * 50)
    print("SCRAPING TERMINÉ")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Scraper de livres depuis books.toscrape.com")
    parser.add_argument("--pages", "-p", type=int, default=DEFAULT_PAGES_TO_SCRAPE,
                        help=f"Nombre de pages à scraper (default: {DEFAULT_PAGES_TO_SCRAPE})")
    parser.add_argument("--no-csv", action="store_true", help="Ne pas sauvegarder en CSV")
    parser.add_argument("--no-db", action="store_true", help="Ne pas sauvegarder en base de données")

    args = parser.parse_args()

    try:
        scrape_and_save(
            pages=args.pages,
            save_csv=not args.no_csv,
            save_db=not args.no_db
        )
    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur. Arrêt du programme.")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
