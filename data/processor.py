# data/processor.py
import pandas as pd

def create_dataframe_from_books(books: list) -> pd.DataFrame:
    """Créer un DataFrame pandas à partir d'une liste de dictionnaires de livres."""
    df = pd.DataFrame(books)
    return df

def save_to_csv(df: pd.DataFrame, filename: str = "books.csv") -> None:
    """Sauvegarder le DataFrame en fichier CSV."""
    df.to_csv(filename, index=False)
    print(f"Données sauvegardées dans {filename}")

def load_from_csv(filename: str = "books.csv") -> pd.DataFrame:
    """Charger un DataFrame à partir d’un fichier CSV."""
    df = pd.read_csv(filename)
    return df
