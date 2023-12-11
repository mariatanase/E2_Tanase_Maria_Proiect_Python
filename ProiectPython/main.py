'''Se va crea un crawler care va lua toate informatiile de pe pagina de laboratoare a site-ului de
python. Pe baza problemelor extrase se vor crea subdirectoare intr-un director specificat, de
forma lab{d}, ce vor contine fisiere de forma: lab{d}.py. In interiorul acestora se vor crea
functiile conform informatiilor de pe pagina. Doar numele functiei in cazul in care exista va fi
luat in considerare, altfel numarul exercitiului de forma: ex{d}. De exemplu:
“”” def ex1(parametru):
pass
“””
INPUT: Directorul unde se vor vrea subdirectoarele cu fisierele .py
Template.py <director>
OUTPUT: Directorul completat cu cerintele de mai sus'''

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

base_url = "https://gdt050579.github.io/python-course-fii/"
current_url = base_url + "labs.html"

while current_url:
    print(current_url)

    response = requests.get(current_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    next_link = soup.find('a', {'rel': 'next'})

    if next_link:
        lab_page = next_link['href']
        next_url = urljoin(current_url, lab_page)
        current_url = next_url
    else:
        current_url = None

