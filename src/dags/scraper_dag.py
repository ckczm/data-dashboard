from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from tasks.collect_job_pages import collect_pagination_links
from tasks.collect_job_links import collect_job_links
from tasks.extract_job_details import extract_job_details
from tasks.filter_and_load_data import filter_load_data

with DAG(
    'scraping_nf',
    default_args={
        'depends_on_past': False,
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        'trigger_rule': 'all_success'
    },
    description='Simple Dag',
    schedule_interval=None,
    start_date=datetime(2021, 1, 1),
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id='collect_pagination_links',
        python_callable=collect_pagination_links,
    )

    t2 = PythonOperator(
        task_id='collect_job_links',
        provide_context=True,
        python_callable=collect_job_links,
    )

    t3 = PythonOperator(
        task_id='extract_job_details',
        python_callable=extract_job_details
    )

    t4 = PythonOperator(
        task_id='filter_load_data',
        python_callable=filter_load_data
    )

    t1 >> t2 >> t3 >> t4
