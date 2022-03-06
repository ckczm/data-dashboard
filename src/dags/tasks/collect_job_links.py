import json
import requests

from io import BytesIO
from minio import Minio
from bs4 import BeautifulSoup


def collect_job_links(ti):
    pagination_links = ti.xcom_pull(
        task_ids="collect_pagination_links",
        dag_id="scraping_nf",
        key="pagination_links"
    )

    all_job_links = {}
    for rel_link in pagination_links:
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
    
    client = Minio(
        endpoint="10.108.27.13:8502",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

    client.make_bucket("job-links")

    json_data = json.dumps(all_job_links)
    binary_data = json_data.encode()
    data_to_send = BytesIO(binary_data)

    client.put_object(
        bucket_name="job-links",
        object_name="links.json",
        data=data_to_send,
        length=len(binary_data)
    )
