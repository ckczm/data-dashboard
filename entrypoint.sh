#!/bin/bash

# SETUP POSTGRES
psql postgresql://postgres:postgres@10.108.27.13:8504 -U postgres -f data-dashboard/src/db/nofluff.sql
echo -e "Nofluffdata database was created."

# SETUP AIRFLOW
airflow db upgrade
airflow users create -e admin@ey.com -f Airflow -l Admin -r Admin -u admin -p password
airflow db init
airflow webserver &
sleep 10
airflow scheduler