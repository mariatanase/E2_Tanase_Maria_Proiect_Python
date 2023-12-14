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

import os
import requests
import re
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin

directory_path = "C:/Users/Maria/PycharmProjects/Python/ProiectPython/labs"

def create_directory_and_python_file(base_directory_path, name):
    try:
        lab_directory = os.path.join(base_directory_path, name)
        if not os.path.exists(lab_directory):
            os.makedirs(lab_directory)
        lab_file = os.path.join(lab_directory, f"{name}.py")
        with open(lab_file, 'w'):
            pass
    except Exception as e:
        print(f"Error occurred: {e}")
    return lab_directory, lab_file

def main(directory_path):
    base_url = "https://gdt050579.github.io/python-course-fii/"
    current_url = base_url + "labs.html"
    next_url = None

    while current_url:
        response = requests.get(current_url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        if next_url:
            title = soup.find('title')
            result = re.search("\d+", title.text)
            lab_number = result.group(0)
            dir_name = "lab" + lab_number
            dir_path, file_path = create_directory_and_python_file(directory_path, dir_name)

            main = soup.find('main')

            ol_elements = main.find_all('ol')
            for ol in ol_elements:
                start = ol.get('start')
                if start:
                    ol_start = int(start)
                else:
                    ol_start = 1

                li_elements = ol.find_all('li')
                for i, li in enumerate(li_elements, start=ol_start):
                    pattern = r'\b(\w+)\s+function\b'
                    match = re.search(pattern, li.text)
                    if match and match.group(1) != 'a' and match.group(1) != 'lambda':
                        func_name = match.group(1)
                    else:
                        func_name = "ex" + str(i)
                    try:
                        with open(file_path, 'a') as file:
                            file.write(f'def {func_name}(parametru):\n    pass\n')
                    except Exception as e:
                        print(f"Error occurred: {e}")


        next_link = soup.find('a', {'rel': 'next'})

        if next_link:
            lab_page = next_link['href']
            next_url = urljoin(base_url, lab_page)
            current_url = next_url
        else:
            current_url = None

if len(sys.argv) != 2:
    print("Number of arguments incorrect")
else:
    directory_path = sys.argv[1]
    main(directory_path)
