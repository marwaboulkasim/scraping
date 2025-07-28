import pandas as pd

def clean_book_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et transforme les données issues du scraping.

    - Convertit les prix en float
    - Extrait les chiffres de la disponibilité
    - Nettoie les colonnes texte si besoin

    Args:
        df (pd.DataFrame): Données brutes issues du scraping

    Returns:
        pd.DataFrame: Données nettoyées prêtes pour l'insertion en base
    """

    # Nettoyage du prix : enlever le symbole £ et convertir en float
    df["price"] = df["price"].replace(r"[^\d.]", "", regex=True).astype(float)

    # Nettoyage de la disponibilité : extraire le nombre d'exemplaires
    df["availability"] = df["availability"].astype(str).str.extract(r"(\d+)").astype(float).fillna(0).astype(int)

    # Nettoyage du titre : supprimer les espaces en trop
    df["title"] = df["title"].str.strip()

    # Nettoyage de la catégorie (si présente)
    if "category" in df.columns:
        df["category"] = df["category"].str.strip()

    # Convertir le rating en entier si c'est sous forme textuelle (optionnel)
    rating_mapping = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["rating"] = df["rating"].map(rating_mapping).fillna(0).astype(int)

    return df
