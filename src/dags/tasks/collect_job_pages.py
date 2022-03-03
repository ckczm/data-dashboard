import requests
from bs4 import BeautifulSoup

def collect_job_pages_links(ti):
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
    ti.xcom_push(key="page_links", value=pages)

def print_pages(ti):
    x = ti.xcom_pull(task_ids="collect_job_pages", dag_id="scraping_nf" , key="page_links")
    print(x)