import json
import requests
from bs4 import BeautifulSoup

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

all_job_links = {}
for rel_link in pages:
    headers = {"user-agent": "lukasz.zywicki@gmail.com"}
    content = requests.get(
        url=f"https://nofluffjobs.com{rel_link}",
        headers=headers
    )
    soup = BeautifulSoup(content.text, "lxml")
    
    job_links = []
    for link in soup.find_all("a"):
        if "/pl/job" in link.get("href"):
            job_links.append(link.get("href"))
    
    key = rel_link.split("?")[1].replace("=", "_")
    all_job_links[key] = job_links

for page in all_job_links.keys():
    for index, link in enumerate(all_job_links[page]):
        headers = {"user-agent": "lukasz.zywicki@gmail.com"}
        content = requests.get(
            url=f"https://nofluffjobs.com{link}",
            headers=headers
        )
        soup = BeautifulSoup(content.text, "lxml")

        requirements = soup.find_all("common-posting-requirements")

        # mandatory requirements
        mandatory_req = []
        for item in requirements[0]:
            for button in item.find_all("button"):
                mandatory_req.append(button.text.strip())

        # nice to have
        nice_to_have_req = []
        try:
            for item in requirements[1]:
                for button in item.find_all("button"):
                    nice_to_have_req.append(button.text.strip())
        except IndexError as exc:
            print(f"There wasn`t any nice to have requirements in offer under link: {link}")

        with open(f"tmp_storage/{page}_link_{index}.json", "w", encoding='utf8') as f:
            data = {
                "job_name": soup.select_one(".posting-details-description").h1.text.strip(),
                "salary": soup.find("common-posting-salaries-list").h4.text.strip(),
                "seniority": soup.find("common-posting-seniority").span.text.strip(),
                "requirements": mandatory_req,
                "nice_to_have": nice_to_have_req
            }
            json.dump(data, f, indent=4, ensure_ascii=False)
