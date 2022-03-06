CREATE DATABASE nofluffdata WITH ENCODING = 'UTF-8';

\connect nofluffdata;

CREATE TABLE job_details (
    id SERIAL PRIMARY KEY,
    job_name VARCHAR(200),
    min_salary INT,
    max_salary INT,
    seniority VARCHAR(150),
    requirements VARCHAR(30)[],
    nice_to_have VARCHAR(30)[]
);