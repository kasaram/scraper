#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import json
from scraping import change_name
import argparse


def argparse_setup():
    '''Setup argparse.'''
    parser = argparse.ArgumentParser()

    parser.add_argument('category',
                        help='the category the product is going to be in',
                        type=str)

    parser.add_argument('url',
                        help='the url to the product',
                        type=str)

    parser.add_argument('--komplett',
                        help='add only komplett-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--proshop',
                        help='add only proshop-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--computersalg',
                        help='add only computersalg-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--elgiganten',
                        help='add only elgiganten-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    parser.add_argument('--avxperten',
                        help='add only avxperten-domain under the product-name,'
                             'if this is the only optional flag',
                        action="store_true")

    return parser.parse_args()


def komplett(link):
    '''Get name of product from Komplett-link.'''
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('div', class_='product-main-info__info').h1.span.text.lower()
    name = change_name(name)
    return name


def proshop(link):
    '''Get name of product from Proshop-link.'''
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('div', class_='col-xs-12 col-sm-7').h1.text.lower()
    name = change_name(name)
    return name


def computersalg(link):
    '''Get name of product from Computersalg-link.'''
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('h1', itemprop='name').text.lower()
    name = change_name(name)
    return name


def elgiganten(link):
    '''Get name of product from Elgiganten-link.'''
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('h1', class_='product-title').text.lower()
    name = change_name(name)
    return name


def avxperten(link):
    '''Get name of product from AvXperten-link.'''
    response = requests.get(link)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    name = html_soup.find('div', class_='content-head').text.strip().lower()
    name = change_name(name)
    return name


def ændre_æøå(navn):
    '''Change the letters æ, ø and å to international letters to avoid unicode.'''
    nyt_navn = ''
    for bogstav in navn:
        if bogstav in 'æøå':
            if bogstav == 'æ':
                bogstav = 'ae'
            elif bogstav == 'ø':
                bogstav = 'oe'
            elif bogstav == 'å':
                bogstav = 'aa'
        nyt_navn += bogstav
    return nyt_navn


def check_arguments():
    '''Check if any of the optional domain arguments is giving to the script
       and returns those that are as one json-object.'''
    json_object = json.loads('{}')
    if args.komplett or args.proshop or args.computersalg or args.elgiganten or args.avxperten:
        if args.komplett:
            json_object.update({
                                    f"{komplett_domain}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.proshop:
            json_object.update({
                                    f"{proshop_domain}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.computersalg:
            json_object.update({
                                    f"{computersalg_domain}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.elgiganten:
            json_object.update({
                                    f"{elgiganten_domain}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
        if args.avxperten:
            json_object.update({
                                    f"{avxperten_domain}": {
                                        "info": {
                                            "part_num": "",
                                            "url": ""
                                        },
                                        "dates": {}
                                    }
                                })
    else:
        json_object = {
                            f"{komplett_domain}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{proshop_domain}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{computersalg_domain}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{elgiganten_domain}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            },
                            f"{avxperten_domain}": {
                                "info": {
                                    "part_num": "",
                                    "url": ""
                                },
                                "dates": {}
                            }
                        }
    return json_object


def save_json(kategori, produkt_navn):
    '''Save (category and) product-name in JSON-file.'''
    with open('records.json', 'r') as json_file:
        data = json.load(json_file)

    with open('records.json', 'w') as json_file:
        if kategori not in data.keys():
            data[kategori] = {}

        data[kategori][produkt_navn] = check_arguments()

        json.dump(data, json_file, indent=2)


def find_domain(link):
    '''Return the domain of the url without "www." and ".dk".'''
    if link == 'www.komplett.dk':
        return 'Komplett'
    elif link == 'www.proshop.dk':
        return 'Proshop'
    elif link == 'www.computersalg.dk':
        return 'Computersalg'
    elif link == 'www.elgiganten.dk':
        return 'Elgiganten'
    elif link == 'www.avxperten.dk':
        return 'AvXperten'


def add_to_scraper(kategori, link, url_domain):
    '''Add line to scraping.py, so scraping.py can scrape the new product.'''
    domain = find_domain(url_domain)

    with open('scraping.py', 'a+') as python_file:
        python_file.write(f'    {domain}(\'{kategori}\', \'{link}\')\n')
        print(f'{kategori}\n{link}')


def main(kategori, link):
    #kategori = input("Kategori f.eks. 'gpu': ")
    #kategori = args.category
    #produkt_navn = input('Produkt navn: ')

    #link = input('Indsæt link fra Komplett, Proshop eller Computersalg\n>')
    #link = args.url
    URL_domain = link.split('/')[2]

    # to determine which kind of site to find product name on
    if URL_domain == komplett_domain:
        produkt_navn = komplett(link)
    elif URL_domain == proshop_domain:
        produkt_navn = proshop(link)
    elif URL_domain == computersalg_domain:
        produkt_navn = computersalg(link)
    elif URL_domain == elgiganten_domain:
        produkt_navn = elgiganten(link)
    elif URL_domain == avxperten_domain:
        produkt_navn = avxperten(link)
    else:
        print(f'Sorry, but I can\'t scrape from this domain: {URL_domain}')
        return

    # Ændre æ, ø og/eller å
    kategori = ændre_æøå(kategori)
    produkt_navn = ændre_æøå(produkt_navn)

    save_json(kategori, produkt_navn)
    add_to_scraper(kategori, link, URL_domain)


if __name__ == '__main__':
    komplett_domain = 'www.komplett.dk'
    proshop_domain = 'www.proshop.dk'
    computersalg_domain = 'www.computersalg.dk'
    elgiganten_domain = 'www.elgiganten.dk'
    avxperten_domain = 'www.avxperten.dk'
    args = argparse_setup()
    main(args.category, args.url)
