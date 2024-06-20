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
        if os.path.exists(filename_default):
            print(f"PDF file is downloaded before - '{filename_default}'")

        else:
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


# base_url = "https://www.cbsl.gov.lk/en/laws/directions-circulars-guidelines-for-non-banks"
# for view-content, need to remove duplicates
tag_class = "view-content"
section = "LAWS"


# folder = "test"
# sources = {
#     "https://www.cbsl.gov.lk/en/laws/directions-circulars-guidelines-on-payments-and-settlements": "cbsl-data\LAWS\Directions, Circulars and Guidelines\Payments and Settlements",
#     "https://www.cbsl.gov.lk/en/laws/directions-circulars-guidelines-on-domestic-operations": "cbsl-data\LAWS\Directions, Circulars and Guidelines\Domestic Operations",
#     "https://www.cbsl.gov.lk/en/laws/directions-circulars-guidelines-on-public-debt": "cbsl-data\LAWS\Directions, Circulars and Guidelines\Public Debt",
#     "https://www.cbsl.gov.lk/en/laws/directions-circulars-guidelines-for-micro-fianace-institutions": "cbsl-data\LAWS\Directions, Circulars and Guidelines\Micro Finance",
# }

# sources = {
#     "https://www.cbsl.gov.lk/en/statistics/economic-indicators/price-report": ("cbsl-data\STATISTICS\Economic Indicators\Daily Price Report", "div"),
#     "https://www.cbsl.gov.lk/en/statistics/economic-indicators/daily-indicators": ("cbsl-data\STATISTICS\Economic Indicators\Daily Indicators", "div"),
#     "https://www.cbsl.gov.lk/en/statistics/economic-indicators/weekly-indicators": ("cbsl-data\STATISTICS\Economic Indicators\Weekly Indicators", "div"),
#     "https://www.cbsl.gov.lk/en/statistics/economic-indicators/monthly-indicators": ("cbsl-data\STATISTICS\Economic Indicators\Monthly Indicators", "div"),
#     "https://www.cbsl.gov.lk/en/statistics/economic-indicators/monthly-bulletin": ("cbsl-data\STATISTICS\Economic Indicators\Monthly Bulletin", "div"),
#     "https://www.cbsl.gov.lk/en/statistics/economic-indicators/macro-economic-chart-pack": ("cbsl-data\STATISTICS\Economic Indicators\Macroeconomic Chart Pack", "div"),
#     "https://www.cbsl.gov.lk/en/statistics/business-surveys/sl-purchasing-managers-index-survey": ("cbsl-data\STATISTICS\Business Surveys\Purchasing Managers' Index", "span")
# }

sources = {
    # "https://www.cbsl.gov.lk/en/press/press-releases/government-securities": ("cbsl-data\PRESS\Press Releases\Government Securities", "span"),
    # "https://www.cbsl.gov.lk/en/press/press-releases/monetary-policy-review": ("cbsl-data\PRESS\Press Releases\Monetary Policy Review", "span"),
    # "https://www.cbsl.gov.lk/en/press/press-releases/external-sector-performance": ("cbsl-data\PRESS\Press Releases\External Sector Performance", "span"),
    # "https://www.cbsl.gov.lk/en/press/press-releases/open-market-operations": ("cbsl-data\PRESS\Press Releases\Open Market Operations", "span"),
    # "https://www.cbsl.gov.lk/en/press/press-releases/inflation": ("cbsl-data\PRESS\Press Releases\Inflation", "span"),
    # "https://www.cbsl.gov.lk/en/press/press-releases/purchasing-managers-index-survey": ("cbsl-data\PRESS\Press Releases\Purchasing Managers Index Survey", "span"),
    # "https://www.cbsl.gov.lk/en/press/press-releases/non-bank-financial-institutions": ("cbsl-data\PRESS\Press Releases/Non-Bank Financial Institutions", "span"),
    # "https://www.cbsl.gov.lk/en/press/press-releases/other": ("cbsl-data\PRESS\Press Releases\Other", "span"),
    # "https://www.cbsl.gov.lk/en/press/media/notices": ("cbsl-data\PRESS\Media/Notices", "span")
}

for url in sources:
    base_url = url
    folder = sources[url][0]
    tag = sources[url][1]

    all_links = []

    for page_num in range(150):
        try:
            driver.get(
                f"{base_url}?page={page_num}")

            print(f"Page - {page_num}")

            page_html = driver.page_source
            page_data = BeautifulSoup(page_html, 'html.parser')

            # div_tag = page_data.find("div", class_=tag_class)
            span_tags = page_data.find_all(tag, class_="field-content")

            pdf_links = {}
            for span in span_tags:
                try:
                    a_tag = span.find("a")
                    if a_tag['href'] not in pdf_links and a_tag['href'] not in all_links:
                        pdf_links[a_tag['href']] = a_tag.get_text().strip()
                        all_links.append(a_tag['href'])
                except:
                    continue

            print(len(pdf_links))
            if len(pdf_links) == 0:
                break

            i = 1
            for key in pdf_links:

                if pdf_links[key] == "":
                    name = f"PDF file {i}.pdf"
                    i += 1
                else:
                    name = f"{pdf_links[key].replace('.', '')}.pdf"
                    name = name.replace("\\", "")
                    name = name.replace("/", "")

                pdf_link = key
                # if base_url not in pdf_link:
                #     pdf_link = base_url+pdf_link
                try:
                    save_pdf(pdf_link, f"{folder}/{name}")
                except:
                    continue

                time.sleep(2)

        except Exception as e:
            print(e)
