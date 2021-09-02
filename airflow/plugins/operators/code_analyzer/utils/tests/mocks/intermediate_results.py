findings = {
    '/thesis-analyzeMe.git_2021-05-16_15:38:48/docker-compose.yaml': {
        'tool': 'docker',
        'traces': {
            'postgres': {
                'env_variables': {
                    'port': '5432',
                    'POSTGRES_USER': 'admin',
                    'POSTGRES_DB': '${db:~dags}',
                    'use_env_files': ['.env'],
                    "db": "test"
                },
                'match': {
                    'storage_modules': ['postgres'],
                    'storage': 'postgres'
                }
            },
            'reporting-db': {
                'env_variables': {
                    'port': '27017',
                    'use_env_files': ['.env']
                },
                'match': {
                    'storage_modules': ['mongo'],
                    'storage': 'mongodb'
                }
            }
        }
    },
    '/thesis-analyzeMe.git_2021-05-16_15:38:48/playbooks/4_pg.yml': {
        'tool': 'ansible',
        'traces': {
            'webservers': {
                'env_variables': {
                    'string_variables': [
                        'db={{dbname}} name={{dbuser}} password={{dbpassword}} priv=ALL',
                        'name={{dbuser}} role_attr_flags=NOSUPERUSER,NOCREATEDB'
                    ],
                    'dbname':
                    'myapp',
                    'dbuser':
                    'django',
                    'dbpassword':
                    'mysupersecretpassword'
                },
                'match': {
                    'storage_modules': ['postgresql_user', 'postgresql_user'],
                    'storage': 'postgres'
                }
            }
        }
    },
}

resolved = {
    '/thesis-analyzeMe.git_2021-05-16_15:38:48/docker-compose.yaml': {
        ('docker', 'postgres', 'postgres-/thesis-analyzeMe.git_2021-05-16_15:38:48/docker-compose.yaml'):
        {
            'storage_modules': ['postgres'],
            'port': '5432',
            'POSTGRES_USER': 'admin',
            'POSTGRES_DB': 'test',
            'use_env_files': ['.env'],
            'db': 'test'
        },
        ('docker', 'mongodb', 'reporting-db-/thesis-analyzeMe.git_2021-05-16_15:38:48/docker-compose.yaml'):
        {
            'storage_modules': ['mongo'],
            'port': '27017',
            'use_env_files': ['.env']
        }
    },
    '/thesis-analyzeMe.git_2021-05-16_15:38:48/playbooks/4_pg.yml': {
        ('ansible', 'postgres', 'webservers-/thesis-analyzeMe.git_2021-05-16_15:38:48/playbooks/4_pg.yml'):
        {
            'storage_modules': ['postgresql_user', 'postgresql_user'],
            'string_variables': [
                'db={{dbname}} name={{dbuser}} password={{dbpassword}} priv=ALL',
                'name={{dbuser}} role_attr_flags=NOSUPERUSER,NOCREATEDB'
            ],
            'dbname':
            'myapp',
            'dbuser':
            'django',
            'dbpassword':
            'mysupersecretpassword',
            'db':
            'myapp',
            'name':
            'django',
            'password':
            'mysupersecretpassword',
            'priv':
            'ALL',
            'role_attr_flags':
            'NOSUPERUSER,NOCREATEDB'
        }
    }
}
