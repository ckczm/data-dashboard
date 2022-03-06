import json
import requests

from bs4 import BeautifulSoup
from minio import Minio
from io import BytesIO


def extract_job_details():
    client = Minio(
        endpoint="10.108.27.13:8502",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

    response = client.get_object(
        bucket_name="job-links",
        object_name="links.json"
    )

    all_job_links = json.loads(response.data)

    client.make_bucket("job-details")

    for i, page in enumerate(all_job_links.keys()):

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

            # nice to have skills
            nice_to_have_req = []
            try:
                for item in requirements[1]:
                    for button in item.find_all("button"):
                        nice_to_have_req.append(button.text.strip())
            except IndexError as exc:
                print(f"There wasn`t any nice to have skills in offer: {link}")

            # prepare job details
            data = {
                "job_name": soup.select_one(".posting-details-description").h1.text.strip(),
                "salary": soup.find("common-posting-salaries-list").h4.text.strip().replace(" ", ""),
                "seniority": soup.find("common-posting-seniority").span.text.strip(),
                "requirements": mandatory_req,
                "nice_to_have": nice_to_have_req
            }

            # save data to minio
            json_data = json.dumps(data, ensure_ascii=False)
            binary_data = json_data.encode()
            data_to_send = BytesIO(binary_data)

            client.put_object(
                bucket_name="job-details",
                object_name=f"jobs-details-from-page-{i}/link_{index}.json",
                data=data_to_send,
                length=len(binary_data)
            )
