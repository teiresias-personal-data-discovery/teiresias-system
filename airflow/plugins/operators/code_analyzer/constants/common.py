from enum import Enum

# files
YML_EXTENSIONS: list = ['yml', 'YML', 'yaml', 'YAML']

# dependencies
ANSIBLE_STORAGE_MODULES: dict = {
    "postgres": ['postgresql_user'],
    "mongodb": ['mongodb_user']
}

DOCKER_HUB_STORAGE_IMAGES: dict = {
    "postgres": ['postgres'],
    "mongodb": ['mongo']
}

DEPENDENCY_MAP = {
    "ansible": ANSIBLE_STORAGE_MODULES,
    "docker": DOCKER_HUB_STORAGE_IMAGES
}


def get_docker_candidates_match(versioned_image):
    image = versioned_image.split(":")[0]
    for storage, images in DOCKER_HUB_STORAGE_IMAGES.items():
        if image in images:
            return {
                "env_variables": {},
                "match": {
                    "storage_modules": [image],
                    "storage": storage
                }
            }
    return {}


def get_ansible_candidates_match(tasks):
    results: dict = {}
    for task in tasks:
        for key, value in task.items():
            for storage, modules in ANSIBLE_STORAGE_MODULES.items():
                if key in modules:
                    results = {
                        **results, "env_variables": {
                            "string_variables": [
                                *results.get("env_variables", {}).get(
                                    "string_variables", []), value
                            ]
                        },
                        "match": {
                            "storage_modules": [
                                *results.get("match", {}).get(
                                    "ansible_modules", []), key
                            ],
                            "storage":
                            storage
                        }
                    }
    return results


TOOL_CHARACTERISTICS: dict = {
    "ansible": {
        # within plays (subset of playbook)
        "mandatory_keys": ['hosts'],
        "section_map": {
            "hosts": "candidate_node_name",
            "tasks": get_ansible_candidates_match,
            "vars": lambda variables: {
                "env_variables": variables or {}
            }
        },
    },
    "docker": {
        # within root level; version key is mandatory from (version > 1):
        "mandatory_keys": ['version', 'services'],
        "section_map": {
            "services": {
                "candidates_node_names": {
                    "image": get_docker_candidates_match,
                    "ports": lambda ports: {
                        "env_variables": {
                            "port": ports[0].split(":")[1]
                        }
                    },
                    "environment": lambda variables: {
                        "env_variables": variables or {}
                    },
                    "env_file": lambda files: {
                        "env_variables": {
                            "use_env_files": files
                        }
                    }
                }
            }
        },
    }
}

STORAGE_CHARACTERISTICS: dict = {
    "docker": {
        "postgres": {
            "env": {
                "POSTGRES_USER": "user",
                "POSTGRES_PASSWORD": "password",
                "POSTGRES_DB": "db"
            },
            "defaults": {
                'port': "5432"
            },
        },
        "mongodb": {
            "env": {
                "MONGO_INITDB_ROOT_USERNAME": "user",
                "MONGO_INITDB_ROOT_PASSWORD": "password",
                "MONGO_INITDB_DATABASE": "db"
            },
            "defaults": {
                'port': "27017"
            },
        },
    },
    "ansible": {
        "postgresql_user": {
            # internal_key: abstract_key
            "env": {
                "db": "db",
                "name": "user",
                "login_user": "user",
                "password": "password",
                "login_password": "password",
                "login_host": 'host',
                "port": 'port'
            },
            # abstract_key: value
            "defaults": {
                'port': "5432",
                "user": "postgres",
            },
        },
        "mongodb_user": {
            # internal_key: abstract_key
            "env": {
                "database": "db",
                "login_host": 'host',
                "name": "user",
                "login_user": "user",
                "password": "password",
                "login_password": "password",
                "login_port": 'port',
                "port": 'port'
            },
            # abstract_key: value
            "defaults": {
                'port': "27017",
                "host": 'localhost'
            },
        },
    }
}
