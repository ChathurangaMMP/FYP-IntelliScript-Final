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


base_url = "https://www.cbsl.gov.lk/gosl-outstanding-debt-securities"
# for view-content, need to remove duplicates
tag_class = "field-item odd"


driver.get(base_url)

page_html = driver.page_source
page_data = BeautifulSoup(page_html, 'html.parser')

# div_tag = page_data.find("div", class_=tag_class)
p_tags_div = page_data.find("div", class_=tag_class)

a_tags = p_tags_div.find_all("a")

report_pages_links = {
    # "annual-reports/annual-report-2017": "Annual Report 2017",
    # "annual-reports/annual-report-2016": "Annual Report 2016",
    # "annual-reports/annual-report-2015": "Annual Report 2015",
    # "annual-reports/annual-report-2014": "Annual Report 2014",
    # "annual-reports/annual-report-2013": "Annual Report 2013",
    # "annual-reports/annual-report-2012": "Annual Report 2012",
    # "annual-reports/annual-report-2011": "Annual Report 2011",
    # "annual-reports/annual-report-2010": "Annual Report 2010",
    # "annual-reports/annual-report-2009": "Annual Report 2009"
}


# for j in range(2022, 2000, -1):
#     report_pages_links[
#         f"https://www.cbsl.gov.lk/en/publications/economic-and-financial-reports/recent-economic-developments/recent-economic-developments-{j}"] = f"Recent Economic Developments {j}"

# for j in range(2023, 2020, -1):
#     report_pages_links[
#         f"https://www.cbsl.gov.lk/en/publications/other-publications/statistical-publications/economic-and-social-statistics-of-sri-lanka/ess-{j}"] = f"Economic and Social Statistics {j}"

for a_tag in a_tags:
    try:
        report_pages_links[a_tag['href']] = a_tag['href'].split("/")[-1]

    except:
        continue

for link in report_pages_links:
    # url = f"https://www.cbsl.gov.lk/en/publications/economic-and-financial-reports/{link}"
    url = f"https://www.cbsl.gov.lk/{link}"
    os.makedirs(
        f"cbsl-data\FINANCIAL SYSTEM\Financial Markets\Government Securities Market\GOSL Outstanding Debt Securities/{report_pages_links[link]}")

    driver.get(url)

    download_page_html = driver.page_source
    download_page_data = BeautifulSoup(download_page_html, 'html.parser')

    div_tag = download_page_data.find("div", class_=tag_class)
    all_as = div_tag.find_all("a")

    i = 1
    for a in all_as:
        pdf_link = a['href']
        pdf_name = a.get_text().strip()

        if "https://www.cbsl.gov.lk" not in pdf_link:
            pdf_link = f"https://www.cbsl.gov.lk{pdf_link}"

        if pdf_name == "":
            pdf_name = f"PDF file {i}.pdf"
            i += 1
        else:
            pdf_name = f"{pdf_name.replace('.', '')}.pdf"
            pdf_name = pdf_name.replace("\\", "")
            pdf_name = pdf_name.replace("/", "")

            # if base_url not in pdf_link:
            #     pdf_link = base_url+pdf_link
        try:
            save_pdf(
                pdf_link, f"cbsl-data\FINANCIAL SYSTEM\Financial Markets\Government Securities Market\GOSL Outstanding Debt Securities/{report_pages_links[link]}/{pdf_name}")
        except:
            continue
