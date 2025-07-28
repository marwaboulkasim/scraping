# get_data/get_scraping_data.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"


def get_soup(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.content, "html.parser")


def extract_book_data(article):
    title = article.h3.a["title"]
    price = article.find("p", class_="price_color").text.strip().replace("£", "").replace("Â", "")
    availability = "In stock" in article.find("p", class_="instock availability").text.strip()
    rating_str = article.p["class"][1]
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    rating = ratings.get(rating_str, 0)
    return {
        "title": title,
        "price": price,
        "availability": int(availability),
        "rating": rating
    }



def scrape_books(pages=1000):
    all_books = []
    for page_num in range(1, pages + 1):
        print(f"Scraping page {page_num}...")
        soup = get_soup(BASE_URL.format(page_num))
        if not soup:
            print(f"Page {page_num} inaccessible.")
            continue
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            book = extract_book_data(article)
            all_books.append(book)
    return pd.DataFrame(all_books)