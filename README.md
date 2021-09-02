# Teiresias 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Discovery and Inventory of Personal Data in Distributed Systems Environments
*Teiresias* is a distributed system, consisting of an Apache Airflow Celery Cluster and an additional Client-Server architecture for semi-automatic discovery and inventory of personal data in distributed systems environments. 
The GDPR-motivated Privacy Enhancing Technology prototype was developed as part of a Bachelor's Thesis at the *Technische Universität Berlin*.


---

- <a href="README.md#section">Deployment</a>

- <a href="README.md#section">Troubleshooting</a>

## Architecture


## User Flow Chart

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

