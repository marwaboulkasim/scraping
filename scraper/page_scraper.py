# scraper/page_scraper.py

from bs4 import BeautifulSoup
from typing import List, Dict
from .html_fetcher import get_books_html, check_page_exists
from .data_extractor import extract_book_info, validate_book_data
from config.settings import CATALOGUE_URL

def get_books_from_page(soup: BeautifulSoup) -> List[BeautifulSoup]:
    """Récupère les balises HTML de chaque livre sur une page."""
    return soup.find_all("article", class_="product_pod") if soup else []

def scrape_single_page(page_number: int) -> List[Dict]:
    """Scrape les livres d'une seule page du catalogue."""
    url = CATALOGUE_URL.format(page_number)

    if not check_page_exists(url):
        print(f"Page {page_number} inaccessible.")
        return []

    soup = get_books_html(url)
    if soup is None:
        print(f"Erreur de récupération pour la page {page_number}")
        return []

    books_data = []
    for book_element in get_books_from_page(soup):
        book_info = extract_book_info(book_element)
        if validate_book_data(book_info):
            books_data.append(book_info)
        else:
            print("Livre ignoré : données invalides.")
    
    print(f"Page {page_number} : {len(books_data)} livres extraits.")
    return books_data

def scrape_books(pages: int, start_page: int = 1) -> List[Dict]:
    """Scrape plusieurs pages de livres à partir d'une page de départ."""
    all_books = []

    for page_num in range(start_page, start_page + pages):
        all_books += scrape_single_page(page_num)

    print(f"{len(all_books)} livres extraits au total.")
    return all_books
