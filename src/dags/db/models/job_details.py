from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()

class JobDetails(Base):
    __tablename__ = "job_details"

    id = Column(Integer, primary_key=True)
    job_name = Column(String(200))
    job_hash = Column(String(8))
    min_salary = Column(Integer)
    max_salary = Column(Integer)
    seniority = Column(String(150))
    requirements = Column(ARRAY(String(30)))
    nice_to_have = Column(ARRAY(String(30)))

    def __init__(
        self,
        job_name: str,
        job_hash: str,
        min_salary: int,
        max_salary: int,
        seniority: str,
        requirements: List[str],
        nice_to_have: List[str]
    ):

        self.job_name = job_name,
        self.job_hash = job_hash,
        self.min_salary = min_salary,
        self.max_salary = max_salary,
        self.seniority = seniority,
        self.requirements = requirements,
        self.nice_to_have = nice_to_have
    
    def __repr__(self):
        return f"JobDetails: {self.id}, {self.job_name}, {self.job_hash}, \
            {self.min_salary}, {self.max_salary}, {self.seniority}, \
                {self.requirements}, {self.nice_to_have}"
