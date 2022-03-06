import requests
from bs4 import BeautifulSoup

def collect_pagination_links(ti):
    headers = {"user-agent": "lukasz.zywicki@gmail.com"}
    content = requests.get(
        url="https://nofluffjobs.com/pl/praca-it/big-data",
        headers=headers
    )
    soup = BeautifulSoup(content.text, "lxml")

    pages = []
    for link in soup.find_all("a"):
        if "page" in link.get("href"):
            pages.append(link.get("href"))
    ti.xcom_push(key="pagination_links", value=pages)
