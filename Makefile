#!make

CONTAINER_NAME = data-dashboard
IMAGE_NAME = data-dashboard-airflow

build:
    docker build -t $(IMAGE_NAME) .

start:
    docker run -d --rm -p 8501:8080 --name $(CONTAINER_NAME) $(IMAGE_NAME)

clean:
    docker rm -f $(CONTAINER_NAME)

shell:
    docker exec -it $(CONTAINER_NAME) bash