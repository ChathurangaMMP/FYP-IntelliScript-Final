from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import base64


def save_pdf(url, filename_default):
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # Attempt to extract the filename from the "Content-Disposition" header
        content_disposition = response.headers.get("content-disposition")
        if content_disposition:
            filename = unquote(content_disposition.split("filename=")[1])
        else:
            # If the header is not present, use a default filename
            filename = filename_default

        # Save the PDF using the extracted or default filename
        with open(filename, 'wb') as pdf_file:
            pdf_file.write(response.content)

        print(f"PDF file downloaded and saved as '{filename}'")
    else:
        print(
            f"Failed to download the PDF. Status code: {response.status_code}")


services = Service(ChromeDriverManager().install())
options = Options()
# options.add_argument('--headless')
options.add_argument("start-maximized")

driver = webdriver.Chrome(service=services, options=options)

with open("navbar_links.json", "r") as json_file:
    links = json.load(json_file)

base_url = "https://www.cbsl.gov.lk"
# for view-content, need to remove duplicates
tag_class_list = ["field-item odd", "view-content"]
section = "LAWS"

for main_folder in links[section]:
    for subfolder in links[section][main_folder]:
        folder = f"cbsl-data/{section}/{main_folder}/{subfolder}"

        time.sleep(3)

        for page_num in range(20):
            try:
                driver.get(
                    f"{links[section][main_folder][subfolder]}?page={page_num}")

                print(f"{main_folder}/{subfolder} - {page_num}")

                page_html = driver.page_source
                page_data = BeautifulSoup(page_html, 'html.parser')

                try:
                    tag_class = tag_class_list[0]
                    div_tag = page_data.find("div", class_=tag_class)
                except:
                    tag_class = tag_class_list[1]
                    div_tag = page_data.find("div", class_=tag_class)

                pdf_links = [a['href'] for a in div_tag.find_all('a')]

                if tag_class == tag_class_list[1]:
                    pdf_links = list(set(pdf_links))

                for i in range(len(pdf_links)):
                    name = f"PDF file {i+1}.pdf"
                    pdf_link = pdf_links[i]
                    if base_url not in pdf_link:
                        pdf_link = base_url+pdf_link

                    save_pdf(pdf_link, f"{folder}/{name}")
                    time.sleep(3)

            except Exception as e:
                print(e)

            break
