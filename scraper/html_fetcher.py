# scraper/html_fetcher.py
"""
Module pour récupérer le contenu HTML d'une page web
"""

import requests
from bs4 import BeautifulSoup

def get_books_html(url: str) -> BeautifulSoup | None:
    """
    Récupère le contenu HTML d'une page.

    Args:
        url (str): URL de la page à récupérer.

    Returns:
        BeautifulSoup | None: L'objet BeautifulSoup si succès, None sinon.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except (requests.RequestException, ValueError) as e:
        print(f"Erreur lors de la récupération de l'URL {url}: {e}")
        return None

def check_page_exists(url: str) -> bool:
    """
    Vérifie si une page web existe (status HTTP 200).

    Args:
        url (str): URL à vérifier.

    Returns:
        bool: True si la page existe, False sinon.
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
