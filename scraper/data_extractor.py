# scraper/data_extractor.py
"""
Module pour extraire les informations d'un livre depuis son élément HTML.
"""

from bs4 import BeautifulSoup
from typing import Dict

def extract_title(book_element: BeautifulSoup) -> str:
    """Extrait le titre du livre."""
    return book_element.h3.a['title'].strip()

def extract_price(book_element) -> float:
    price_text = book_element.find("p", class_="price_color").text.strip()
    # Supposons que price_text = "£51.77" ou avec un encodage bizarre "Â£51.77"
    
    # Nettoyage : retirer tous les caractères sauf chiffres et '.'
    import re
    cleaned = re.sub(r"[^\d.]", "", price_text)  # garde uniquement chiffres et point
    
    try:
        price = float(cleaned)
    except ValueError:
        price = 0.0  # ou autre valeur par défaut
    
    return price



def extract_rating(book_element: BeautifulSoup) -> int:
    """Extrait la note (rating) du livre sous forme d'entier (1 à 5)."""
    rating_class = book_element.find("p", class_="star-rating")["class"]
    ratings_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    # Le deuxième élément de la classe est la notation textuelle
    for r in ratings_map:
        if r in rating_class:
            return ratings_map[r]
    return 0

def extract_availability(book_element: BeautifulSoup) -> int:
    """Extrait la disponibilité (nombre en stock)."""
    availability_text = book_element.find("p", class_="instock availability").text.strip()
    # Souvent c'est comme 'In stock (22 available)'
    import re
    match = re.search(r"\((\d+) available\)", availability_text)
    return int(match.group(1)) if match else 0

def extract_book_info(book_element: BeautifulSoup) -> Dict:
    """Extrait toutes les informations clés d'un livre sous forme de dictionnaire."""
    return {
        "title": extract_title(book_element),
        "price": extract_price(book_element),
        "rating": extract_rating(book_element),
        "availability": extract_availability(book_element),
    }

def validate_book_data(book_data: Dict) -> bool:
    """
    Valide que les données extraites d'un livre sont complètes et cohérentes.

    Args:
        book_data (Dict): Dictionnaire des données du livre.

    Returns:
        bool: True si valide, False sinon.
    """
    if not book_data["title"]:
        return False
    if book_data["price"] < 0:
        return False
    if not (0 <= book_data["rating"] <= 5):
        return False
    if book_data["availability"] < 0:
        return False
    return True
