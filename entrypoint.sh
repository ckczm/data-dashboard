#!/bin/bash

airflow db upgrade
airflow users create -e admin@ey.com -f Airflow -l Admin -r Admin -u admin -p password
airflow db init
airflow webserver &
sleep 10
airflow scheduler