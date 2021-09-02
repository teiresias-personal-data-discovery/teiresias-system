# Teiresias 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Discovery and Inventory of Personal Data in Distributed Systems Environments
*Teiresias* is a distributed system, consisting of an Apache Airflow Celery Cluster and an additional Client-Server architecture for semi-automatic discovery and inventory of personal data in distributed systems environments. 
The GDPR-motivated Privacy Enhancing Technology prototype was developed as part of a Bachelor's Thesis at the *Technische Universität Berlin*.


---

- <a href="https://github.com/teiresias-personal-data-discovery/teiresias-system/blob/210ab7e60a93b9a0cc675f84be6e4ce25640ed99/docs/deployment.md#deployment">Deployment</a>

- <a href="https://github.com/teiresias-personal-data-discovery/teiresias-system/blob/main/docs/troubleshooting.md#troubleshooting
">Troubleshooting</a>

## Architecture
![Architecture](https://user-images.githubusercontent.com/38670508/131920658-58dee1ba-4534-4036-acea-c5dc32f8c338.png)

## User Flow Chart
![TeiresiasUX](https://user-images.githubusercontent.com/38670508/131920450-6c3f5ec2-b406-48d2-94cf-85d90a0c6ed4.png)

## Project Map
```
.
├── LICENSE . . . . . . . . . . . . . . . . . .   MIT license
├── README.md
├── airflow . . . . . . . . . . . . . . . . . .   Workflow management platform
│   ├── dags                                          ▶ Workflows/DAGs
│   ├── logs                                          ▶ Logs
│   ├── plugins
│   │   └── operators                                 ▶ Custom Operators
│   └── repositories                                  ▶ Directory for code Analysis 
│       └── paste_analyzable_code_here                  ▶ watched directory 
├── certs . . . . . . . . . . . . . . . . . . .   Directory for cert.pem, key.pem
├── docker-compose.yaml     
├── interfaces  . . . . . . . . . . . . . . . .   Inventory GUI & Extension Interface
│   ├── server                                        ▶ NGINX config
│   └── src                                           ▶ React source code
├── inventory-api . . . . . . . . . . . . . . .   Inventory API
│   └── src                                           ▶ NestJS source code
├── inventory-db  . . . . . . . . . . . . . . .   Inventory DB (MongoDB) config
└── reverse-proxy . . . . . . . . . . . . . . .   Reverse proxy (Traefik) config
```
