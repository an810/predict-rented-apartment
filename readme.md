Running Airflow in Docker
Step 1: Initialize Airflow metadata DB
```docker-compose run --rm airflow-webserver airflow db init```

Step 2: Create user
```
docker-compose run --rm airflow-webserver airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

Step 3: Start Airflow
```docker-compose up -d```

