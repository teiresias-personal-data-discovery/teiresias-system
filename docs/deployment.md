## Deployment

- Prerequisite
  - Unix host with min. 16GB RAM (Tested on macOS 10.14, Ubuntu 20.04)
  - Docker (20.10+), Docker Compose (1.27+)

- Clone this Git respository to target host
- Follow steps _Preparation_, _Build & Run_, _Integration and Configuration_

### ▶ Preparation
- Replace `.env.sample` with `.env`
  - special requirements:
    - _AIRFLOW__CORE__FERNET_KEY_: 32 url-safe base64-encoded bytes
    - _MONGO_INVENTORYUSER_PWDHASH_: hashed password, incl. salt; using bycryptjs' *bcrypt.hashSync(\<password>, 12)*

- Certificate / Domains

  - Generate `certs/cert.pem`, `certs/key.pem `
    - locally e.g. via [*mkcert*](https://github.com/FiloSottile/mkcert), which creates files and a local CA by:
      ```bash
      $ mkcert -install
      $ mkcert -cert-file certs/cert.pem -key-file certs/key.pem "docker.localhost" "*.docker.localhost"
      ```
      predefined local URLs
        - Interfaces: https://interfaces.docker.localhost/
        - Inventory-API: https://inventory-api.docker.localhost/
        - Airflow Web Server: https://airflow.docker.localhost/
        - Flower Celery Monitoring: https://flower.docker.localhost/
        - Traefik Reverse Proxy Server: https://traefik.docker.localhost/


    - Deployment, using Domain
      - Generate files & adjust domain settings in `reverse-proxy/config.yaml` and `.env`


- On Linux host, adjust file permissions for bind mount volumes `airflow/dags`, `airflow/logs`, `airflow/plugins`, `airflow/repositories`
  - set `.env`-variable _AIRFLOW_GID_ to unused groupId (e.g. 50000) within host
  - 
    ```bash
    # replace <AIRFLOW_GID> with groupId which was set in the prior step 
    $ sudo chown :<AIRFLOW_GID> airflow/dags airflow/logs airflow/plugins airflow/repositories 
    $ sudo chmod 775 airflow/dags airflow/logs airflow/plugins airflow/repositories 
    $ sudo chmod g+s airflow/dags airflow/logs airflow/plugins airflow/repositories 
    ```
  
  - (inspired by:  https://medium.com/@nielssj/docker-volumes-and-file-system-permissions-772c1aee23ca, Visited on 2021-08-31)

### ▶ Build & Run
```bash
# create network
$ docker network create proxy
# build images
$ docker-compose build
# initialize Airflow metaDB
$ docker-compose up airflow-init
# start Teiresias
$ docker-compose up
```

### ▶ Integration and Configuration
- Code Analysis of IaC Git repository: Enable access to repository hosting service:
    - get public key of Airflow user
      ```bash
      # while system is running, copy public key from second terminal
      <your_host> $ docker exec -it airflow-webserver bash
      # on the container, print public key on bash
      <container> $ cat ~/.ssh/id_rsa.pub
      # copy to clipboard
      ```

    - paste public key to access control SSH-key section of your repository hosting service (e.g. GitHub: to SSH section of user with access, Bitbucket: to SSH section of repository)
- Enable network access to all hosts which have to be examined, such as Databases
- Workflows; configure from Airflow Web Server GUI:
  - unpause all Airflow DAGs
  - start (trigger manually) DAG _A2_manually_code_analysis_ to enable filesystem-sensoring in order to analyse manually pasted IaC 
