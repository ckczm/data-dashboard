import requests
from bs4 import BeautifulSoup

# headers = {"user-agent": "lukasz.zywicki@gmail.com"}
# content = requests.get(
#     url="https://nofluffjobs.com/pl/praca-it/big-data",
#     headers=headers
# )
# soup = BeautifulSoup(content.text, "lxml")

# page_links = []
# for link in soup.find_all("a"):
#     if "page" in link.get("href"):
#         page_links.append(link.get("href"))

# all_job_links = {}
# for rel_link in page_links:
#     headers = {"user-agent": "lukasz.zywicki@gmail.com"}
#     content = requests.get(
#         url=f"https://nofluffjobs.com{rel_link}",
#         headers=headers
#     )
#     soup = BeautifulSoup(content.text, "lxml")
    
#     job_links = []
#     for link in soup.find_all("a"):
#         if "/pl/job" in link.get("href"):
#             job_links.append(link.get("href"))
    
#     key = rel_link.split("?")[1]
#     all_job_links[key] = job_links

# print(all_job_links)

headers = {"user-agent": "lukasz.zywicki@gmail.com"}
content = requests.get(
    url="https://nofluffjobs.com/pl/praca-it/big-data",
    headers=headers
)
soup = BeautifulSoup(content.text, "lxml")
for link in soup.find_all("a"):
    if "/pl/job" and "erwin" in link.get("href"):
        print(link.get("href"))
        print(link.contents[3].h3.string)
        print(link.contents[4].span.text)
