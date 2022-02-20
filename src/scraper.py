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
    url="https://nofluffjobs.com/pl/job/data-architect-with-data-modeling-erwin-devire-remote-tfvhi8l3",
    headers=headers
)
soup = BeautifulSoup(content.text, "lxml")
# for link in soup.find_all("a"):
#     if "/pl/job" and "erwin" in link.get("href"):
#         print(link.get("href"))
#         print(link.contents[3].h3.string)
#         print(link.contents[4].span.text)
print(soup.select_one(".posting-details-description").h1.text)
print(soup.find("common-posting-salaries-list").h4.text)
print(soup.find("common-posting-seniority").span.text)
# print(soup.find("common-posting-requirements").h3)

requirements = soup.find_all("common-posting-requirements")

# mandatory requirements
mandatory_req = set()
for item in requirements[0]:
    for button in item.find_all("button"):
        mandatory_req.add(button.text)

# nice to have
nice_to_have_req = set()
for item in requirements[1]:
    for button in item.find_all("button"):
        nice_to_have_req.add(button.text)

print(f"Mandatory requirements: {mandatory_req}")
print(f"Nice to have: {nice_to_have_req}")
