import requests
from bs4 import BeautifulSoup
import pandas as pd

# On récupère le contenu HTML d’une page
url = "http://books.toscrape.com/"
response = requests.get(url)

# On stocke le contenu HTML dans une variable
html_content = response.content

# On crée un objet BeautifulSoup pour parser le HTML
soup = BeautifulSoup(html_content, "html.parser")

# Affichage des mille premier caractères du HTML formaté
print(soup.prettify()[:1000])

# Affiche la balise <title>...</title>
print(soup.title)

# On accède à la balise <title> et on l'affiche
print(soup.title.text)
print(soup.find("h1")) 

# Récupérer tous les titres de livres de la page d’accueil

# Chaque livre est dans une balise <article class="product_pod">
# On utilise find_all pour trouver toutes les balises correspondantes
# On peut ensuite accéder aux informations de chaque livre
books = soup.find_all("article", class_="product_pod")

# On affiche les informations récoltées sur le premier livre de la liste
first_book = books[0]
print(first_book)


# On affiche le titre du premier livre
title_first_book = books[0].find("h3").find("a")["title"]
print(title_first_book)

# On parcourt la liste des livres et on affiche le titre de chacun
for book in books:
    title = title_book = book.find("h3").find("a")["title"]
    print(title)

    # Liste des titres de livres en utilisant la compréhension de liste
titles_list =  [book.find("h3").find("a")["title"] for book in books]
print(titles_list)

# Nombre de livres trouvés
books_nb = books.__len__() 
print(f"Nombre de livres trouvés : {books_nb}")

# Prix du premier livre
price_first_book = books[0].find("p", class_="price_color").text
print(f"Prix du premier livre : {price_first_book}")

# Afficher la note (rating) du premier livre
rating_first_book = books[0].find("p", class_="star-rating")["class"][1]
print(f"Note du premier livre : {rating_first_book}")

# Pour chaque livre, on souhaite afficher : le prix, le titre et la disponibilité
for book in books:
    title = title_book = book.find("h3").find("a")["title"]
    price = book.find("p", class_="price_color").text
    availability = book.find("p", class_="instock availability").text.strip()
    print(f"Titre : {title}, Prix : {price}, Disponibilité : {availability}")


    ## 2. Fonctions python d'extraction des données
# Fonction pour extraire le titre d'un livre

"""Extract the title of a book from a BeautifulSoup object.

    Args:
        book (BeautifulSoup): The HTML element of the book.

    Returns:
        str: The title of the book.

def extract_title(book: BeautifulSoup) -> str:
 for book in books:
    return book.find("h3").find("a")["title"] 
print(extract_title(books[0]))
  """


def extract_title(book: BeautifulSoup) -> str:
    return book.find("h3").find("a")["title"] 
print(extract_title(books[0]))

# Fonction pour extraire le prix d'un livre
def extract_price(book: BeautifulSoup) -> str:
    return book.find("p", class_="price_color").text
print(extract_price(books[0]))



"""Extract the price of a book from a BeautifulSoup object.

    Args:
        book (BeautifulSoup): The HTML element of the book.

    Returns:
        str: The price of the book.
    """

  # Fonction pour extraire la note d'un livre
"""Extract the rating of a book from a BeautifulSoup object.

    Args:
        book (BeautifulSoup): The HTML element of the book.

    Returns:
        str: The rating of the book.
    """
def extract_rating(book: BeautifulSoup) -> str:
    return book.find("p", class_="star-rating")["class"][1]
print(extract_rating(books[0]))

# Fonction pour extraire la disponibilité d'un livre
def extract_availability(book: BeautifulSoup) -> str:
    """Extract the availability of a book from a BeautifulSoup object.

    Args:
        book (BeautifulSoup): The HTML element of the book.

    Returns:
        str: The availability of the book.
    """
def extract_availability(book: BeautifulSoup) -> str:
    return book.find("p", class_="instock availability").text.strip()
print(extract_availability(books[0]))


# Fonction qui combine les informations d'un livre dans un dictionnaire
def extract_book_info(book: BeautifulSoup) -> dict:
    """Extract all information of a book from a BeautifulSoup object.

    Args:
        book (BeautifulSoup): The HTML element of the book.

    Returns:
        dict: A dictionary containing the title, price, rating, and availability of the book.
    """
def extract_book_info(book: BeautifulSoup) -> dict:
    return {
        "title": extract_title(book),
        "price": extract_price(book),
        "rating": extract_rating(book),
        "availability": extract_availability(book)
    }
print(extract_book_info(books[0]))

# Création d'une liste de dictionnaires contenant les informations de chaque livre
data_books = [{
    "title": book.h3.a["title"],
    "price": book.find("p", class_="price_color").text,
    "availability": book.find("p", class_="instock availability").text.strip()
} for book in books]

# Affichage des 5 premiers livres
print(data_books[:5])


    # Création d'un DataFrame à partir de la liste

df_books = pd.DataFrame(data_books)

# Afficher le début du DataFrame
print(df_books.head())

 ## 3. Itération sur plusieurs pages HTML

 """Fetch the HTML content of a book page.

    Args:
        url (str): The URL of the book page.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the HTML content.
     """
def get_books_html(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def get_books_from_page(soup: BeautifulSoup) -> list:
    books = soup.find_all("article", class_="product_pod")
    return [extract_book_info(book) for book in books]

def extract_book_info(book) -> dict:
    return {
        "title": book.h3.a["title"],
        "price": book.find("p", class_="price_color").text,
        "rating": book.p["class"][1],
        "availability": book.find("p", class_="instock availability").text.strip()
    }
print(get_books_from_page(soup))



# Test de la fonction get_book_html avec la page 2
get_books_html("http://books.toscrape.com/catalogue/page-2.html")

import requests
from bs4 import BeautifulSoup

# Variable de base (corrigée)
base_url = "http://books.toscrape.com/catalogue/page-{}.html"

# 1. Récupération du HTML
def get_books_html(url: str) -> BeautifulSoup:
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")

# 2. Trouver tous les livres sur une page
def get_books_from_page(soup: BeautifulSoup) -> list[BeautifulSoup]:
    return soup.find_all("article", class_="product_pod")

# 3. Extraire les infos d’un seul livre
def extract_title(book: BeautifulSoup) -> str:
    return book.find("h3").find("a")["title"]

def extract_price(book: BeautifulSoup) -> str:
    return book.find("p", class_="price_color").text

def extract_rating(book: BeautifulSoup) -> str:
    return book.find("p", class_="star-rating")["class"][1]

def extract_availability(book: BeautifulSoup) -> str:
    return book.find("p", class_="instock availability").text.strip()

def extract_book_info(book: BeautifulSoup) -> dict:
    return {
        "title": extract_title(book),
        "price": extract_price(book),
        "rating": extract_rating(book),
        "availability": extract_availability(book)
    }

# 4. Scraping sur plusieurs pages
def scrape_books(pages: int) -> list[dict]:
    all_books = []

    for page in range(1, pages + 1):
        url = base_url.format(page)  # Construire l’URL
        soup = get_books_html(url)
        books_tags = get_books_from_page(soup)

        # Compréhension de liste pour extraire les infos
        data_books = [extract_book_info(book) for book in books_tags]

        # Ajouter à la liste globale
        all_books.extend(data_books)

    return all_books

# Test sur les 2 premières pages
books_data = scrape_books(2)
print(books_data)

# Test de la fonction scrape_books avec 50 pages
data_books = scrape_books(50)
print(scrape_books(50)[:5])  

# Création d'un DataFrame à partir de la liste

df_books = pd.DataFrame(data_books)
print(df_books.head((5))) 

# Nombre de livres scrapés
books_nb = len(data_books)
print(f"Nombre de livres scrapés : {books_nb}")

# Sauvegarder les données dans un fichier csv
df_books.to_csv("books_data.csv", index=False)
print("Données sauvegardées dans 'books_data.csv'.")
