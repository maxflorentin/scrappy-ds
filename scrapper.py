import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = 'https://www.digitalsport.com.ar/'

def scrape_products(url, max_price):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('a', class_='product')

    for product in products:
        product_url = urljoin(base_url, product['href'])
        precio = product.find(class_='precio').text.strip()
        precio_numerico = float(precio.replace('$', '').replace(',', ''))

        if precio_numerico < max_price:
            print(f"URL: {product_url}")
            print(f"Precio: {precio}")
            print()

    loadmore_div = soup.find('div', id='loadmore')

    if loadmore_div and loadmore_div.find('a'):
        loadmore_url = loadmore_div.find('a')['href']
        next_url = urljoin(base_url, loadmore_url)
        scrape_products(next_url, max_price)

# Configuración del argumento de línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument('url', type=str, help='URL del sitio web')
parser.add_argument('max_price', type=float, help='Precio máximo')
args = parser.parse_args()

url = args.url
max_price = args.max_price
scrape_products(base_url, max_price)
