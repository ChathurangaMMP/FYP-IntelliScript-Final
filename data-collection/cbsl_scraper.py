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


def download_page_pdf(pdf, filename):
    # Serialize the dictionary to a JSON string.
    json_string = json.dumps(pdf)

    # Decode the JSON string to a bytes-like object.
    pdf_bytes = base64.b64decode(json_string)

    # Write the bytes-like object to the file.
    with open(f"{filename}.pdf", "wb") as f:
        f.write(pdf_bytes)


services = Service(ChromeDriverManager().install())
options = Options()
# options.add_argument('--headless')
options.add_argument("start-maximized")

driver = webdriver.Chrome(service=services, options=options)

base_url = "https://www.cbsl.gov.lk/en"

driver.get(base_url)
time.sleep(2)

# pdf = driver.execute_cdp_cmd("Page.printToPDF", {})

home_page_html = driver.page_source

home_page_data = BeautifulSoup(home_page_html, 'html.parser')

navbar_menu = {}

navbar_ul_class = "tb-megamenu-nav nav level-0 items-9"
navbar_ul_li_classes = ["tb-megamenu-item level-1 mega dropdown active active-trail",
                        "tb-megamenu-item level-1 mega mega-align-justify dropdown"]

main_text_a_class = "dropdown-toggle"
navbar_submenu_li_class = "tb-megamenu-item level-2 mega mega-group"

main_navbar_ul = home_page_data.find_all("ul", class_=navbar_ul_class)[0]

navbar_menu_li = main_navbar_ul.find_all(
    "li", class_=navbar_ul_li_classes[0])+main_navbar_ul.find("li", class_=navbar_ul_li_classes[1])

for menu_item in navbar_menu_li:
    menu_item_text = menu_item.find(
        'a', class_=main_text_a_class).get_text().strip()

    navbar_menu[menu_item_text] = {}

    submenu_li_list = menu_item.find_all("li", class_=navbar_submenu_li_class)
    for li_tag in submenu_li_list:
        submenu_topic = li_tag.find(
            "a", class_="mega-group-title").get_text().strip()
        navbar_menu[menu_item_text][submenu_topic] = {}
        for a_tag in li_tag.find_all("a")[1:]:
            url = a_tag.get('href')
            text = a_tag.get_text().strip()
            navbar_menu[menu_item_text][submenu_topic][text] = base_url[:-3] + url

with open("navbar_links.json", "w") as f:
    json.dump(navbar_menu, f)
