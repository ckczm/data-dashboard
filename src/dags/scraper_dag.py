from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from tasks.collect_job_pages import collect_job_pages_links, print_pages

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
        task_id='collect_job_pages',
        python_callable=collect_job_pages_links,
    )

    t2 = PythonOperator(
        task_id='print_pages',
        provide_context=True,
        python_callable=print_pages,
    )

    t1 >> t2
