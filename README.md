# data_dashboard
1. docker build -t data-dashboard-airflow .
2. docker run -d --rm -p 8501:8080 --name data-dashboard data-dashboard-airflow