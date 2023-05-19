import requests
from bs4 import BeautifulSoup
import json

smartphones_brands_file = open('smartphones_&_brands.json', 'w', 1, 'utf8')
smartphones_brands_dict = {}
all_brands = []

def get_products(products, page, all_prods) :
    product = {}
    for prod in products :

        product['productLink'] = f"https://www.jumia.com.tn{prod.contents[0]['href']}"
        product['productBrand'] = prod.contents[0]['data-brand']
        product['productImage'] = prod.contents[0].find_all('div', {'class': 'img-c'})[0].contents[0]['data-src']
        product['productName'] = prod.contents[0].find_all('div', {'class': 'info'})[0].find('h3', {'class': 'name'}).text
        product['productPrice'] = prod.contents[0].find_all('div', {'class': 'info'})[0].find('div', {'class': 'prc'}).text
        product['minimumPrice'] = prod.contents[0]['data-price']

        all_prods.append(product)

        product = {}

def get_brands(brands) :
    _brand = {}
    for brand in brands :
        _brand['brandName'] = brand.text
        all_brands.append(_brand)
        _brand = {}

    smartphones_brands_dict['brands'] = all_brands

def main() :
    counter = 0
    for page in range(1, 15) :
        URL = f"https://www.jumia.com.tn/smartphones/?page={page}";

        page_content = requests.get(URL).content

        soup = BeautifulSoup(page_content, 'html.parser')

        products = soup.find_all('article', {'class': 'prd _fb col c-prd'})

        all_prods = []
        get_products(products, page, all_prods)

        smartphones_brands_dict[f"page_{page}"] = all_prods

        counter = counter + len(all_prods)

    brands = soup.find_all('div', {'class': '-phs -pvxs -df -d-co -h-168 -oya -sc'})[0].contents
    get_brands(brands)

    smartphones_brands_dict['productsCounter'] = f"{counter} resultat"


    print(json.dumps(smartphones_brands_dict, indent=4))

    smartphones_brands_file.write(f"{smartphones_brands_dict}")
    smartphones_brands_file.close()

main()