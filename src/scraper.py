import requests
from bs4 import BeautifulSoup

headers = {"user-agent": "lukasz.zywicki@gmail.com"}
content = requests.get(
    url="https://nofluffjobs.com/pl/praca-it/big-data?page=1",
    headers=headers
)
soup = BeautifulSoup(content.text, "lxml")
for link in soup.find_all("a"):
    if "/pl/job" and "erwin" in link.get("href"):
        print(link.get("href"))
        print(link.contents[3].h3.string)