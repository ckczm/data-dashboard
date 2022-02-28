FROM apache/airflow:2.2.4-python3.8

USER airflow
RUN mkdir data-dashboard
COPY --chown=airflow:root src/dags/ /opt/airflow/dags/
COPY --chown=airflow:root src/pythonenv/ data-dashboard/src/pythonenv/
COPY --chown=airflow:root entrypoint.sh data-dashboard/entrypoint.sh

RUN pip install apache-airflow==2.1.4 \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.1.4/constraints-3.7.txt"
RUN pip install -r data-dashboard/src/pythonenv/requirements.txt

RUN chmod +x data-dashboard/entrypoint.sh
ENTRYPOINT ["data-dashboard/entrypoint.sh"]