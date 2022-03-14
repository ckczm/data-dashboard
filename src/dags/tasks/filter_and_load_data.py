import json
import pandas as pd

from minio import Minio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models.job_details import JobDetails


def filter_load_data():
    client = Minio(
        endpoint="10.108.27.13:8502",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

    # get all job detail files
    response = client.list_objects(
        bucket_name="job-details",
        recursive=True
    )

    # set db conn
    engine = create_engine('postgresql://postgres:postgres@10.108.27.13:8504/nofluffdata')
    Session = sessionmaker(bind=engine)
    session = Session()

    # get job details from minio and filter data
    for obj in response:
        resp = client.get_object(
            bucket_name="job-details",
            object_name=obj.object_name
        )

        # remove non-breaking spaces
        raw_data = resp.data.decode("UTF-8").replace(u"\u00A0", " ")

        data = json.loads(raw_data)

        # check if job hash already exists in database, if so - skip getting data
        if session.query(JobDetails).filter_by(job_hash=data["job_hash"]).first() is not None:
            continue

        # split salary range into min and max salary value, from max salary
        # remove currency value
        if "-" in data["salary"]:
            split_salary_values = data["salary"].split("-")
            data["min_salary"] = int(split_salary_values[0].replace(" ", ""))
            data["max_salary"] = int(split_salary_values[1][0:-3].replace(" ", "")) # remove PLN
            
            # load data to database
            df = pd.DataFrame([data])
            for _, row in df.iterrows():
                doc = JobDetails(
                    job_name=row["job_name"],
                    min_salary=row["min_salary"],
                    max_salary=row["max_salary"],
                    seniority=row["seniority"],
                    requirements=row["requirements"],
                    nice_to_have=row["nice_to_have"]
                )

                session.add(doc)
                session.commit()
        else:
            print(f"Non-standard salary value: {data['salary']}")

    session.close()
