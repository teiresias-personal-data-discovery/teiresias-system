## Troubleshooting
  
- Symptom: 
    > FATAL: role "airflow" does not exist @airflow-init or airflow-webserver docker container 
  - Reason: The PostgreSQL user name (_POSTGRES_USER_ in _AIRFLOW__CORE__SQL_ALCHEMY_CONN_, _AIRFLOW__CELERY__RESULT_BACKEND_) must not be different from 'airflow'

- Symptom:  
  Airflow web server (API & GUI) unreachable
  - Solution 
    ```bash
    # while system is running, restart airflow-webserver from second terminal
    $ docker-compose stop airflow-webserver && docker-compose up -d airflow-webserver
    ```