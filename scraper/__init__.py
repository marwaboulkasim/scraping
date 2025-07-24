# scraper/__init__.py
"""
Module de scraping pour le site books.toscrape.com
"""

from .html_fetcher import get_books_html, check_page_exists
from .data_extractor import extract_book_info, extract_title, extract_price, extract_rating, extract_availability, validate_book_data
from .page_scraper import scrape_books, get_books_from_page, scrape_single_page

__all__ = [
    'get_books_html',
    'check_page_exists',
    'extract_book_info',
    'extract_title',
    'extract_price',
    'extract_rating',
    'extract_availability',
    'validate_book_data',
    'scrape_books',
    'get_books_from_page',
    'scrape_single_page',
]
