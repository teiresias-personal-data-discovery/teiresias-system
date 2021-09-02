# parsed postgres.yml from git@github.com:ansible/ansible-examples.git
parsed_playbook_yaml_postgres = [{
    'hosts':
    'webservers',
    'become':
    'yes',
    'gather_facts':
    'no',
    'tasks': [{
        'name': 'ensure apt cache is up to date',
        'apt': 'update_cache=yes'
    }, {
        'name': 'ensure packages are installed',
        'apt': 'name={{item}}',
        'with_items': ['postgresql', 'libpq-dev', 'python-psycopg2']
    }]
}, {
    'hosts':
    'webservers',
    'become':
    'yes',
    'become_user':
    'postgres',
    'gather_facts':
    'no',
    'vars': {
        'dbname': 'myapp',
        'dbuser': 'django',
        'dbpassword': 'mysupersecretpassword'
    },
    'tasks': [{
        'name': 'ensure database is created',
        'postgresql_db': 'name={{dbname}}'
    }, {
        'name':
        'ensure user has access to database',
        'postgresql_user':
        'db={{dbname}} name={{dbuser}} password={{dbpassword}} priv=ALL'
    }, {
        'name':
        'ensure user does not have unnecessary privilege',
        'postgresql_user':
        'name={{dbuser}} role_attr_flags=NOSUPERUSER,NOCREATEDB'
    }, {
        'name':
        'ensure no other user can access the database',
        'postgresql_privs':
        'db={{dbname}} role=PUBLIC type=database priv=ALL state=absent'
    }]
}]

parsed_playbook_yaml_mongodb = [{
    'hosts':
    '$servername',
    'remote_user':
    'root',
    'tasks': [{
        'name':
        'Create a new database and user',
        'mongodb_user':
        'login_user=admin login_password={{mongo_admin_pass} login_port={{mongos_port}} database=test user=admin password={{mongo_admin_pass}} state=present'
    }, {
        'name': 'Pause for the user to get created and replicated',
        'pause': 'minutes=3'
    }, {
        'name':
        'Execute the collection creation script',
        'command':
        '/usr/bin/mongo localhost:{{mongos_port}}/test -u admin -p {{mongo_admin_pass}} /tmp/testsharding.js'
    }, {
        'name':
        'Enable sharding on the database and collection',
        'command':
        '/usr/bin/mongo localhost:{{mongos_port}}/admin -u admin -p {{mongo_admin_pass}} /tmp/enablesharding.js'
    }]
}]

parsed_playbook_yaml_mongodb_postgres = [{
    'hosts': 'vagrant',
    'user': 'root',
    'roles': ['sysadmin-centos']
}, {
    'hosts':
    'RDB1',
    'become':
    'yes',
    'become_user':
    'postgres',
    'gather_facts':
    'no',
    'vars': {
        'dbname': 'myapp',
        'dbuser': 'django',
        'dbpassword': 'mysupersecretpassword'
    },
    'tasks': [{
        'name': 'ensure database is created',
        'postgresql_db': 'name={{dbname}}'
    }, {
        'name':
        'ensure user has access to database',
        'postgresql_user':
        'db={{dbname}} name={{dbuser}} password={{dbpassword}} priv=ALL'
    }]
}, {
    'hosts':
    'data',
    'become':
    'yes',
    'become_user':
    'admin',
    'gather_facts':
    'no',
    'vars': {
        'dbname': 'user_collections',
        'login_user': 'nosqler',
        'mongo_admin_pass': 'wysiwyg'
    },
    'tasks': [{
        'name':
        'Create a new database and user',
        'mongodb_user':
        'login_user=admin login_password={{mongo_admin_pass}} login_port={{mongos_port}} database=test user=admin password={{mongo_admin_pass}} state=present'
    }]
}]

parsed_docker_compose_mongodb_postgres: dict = {
    'version': '3',
    'services': {
        'postgres': {
            'image': 'postgres:13',
            'ports': ['5432:5432'],
            'env_file': ['.env'],
            'environment': {
                'POSTGRES_USER': 'admin',
                'POSTGRES_DB': '${db:~dags}'
            },
            'volumes': ['postgres-db-volume:/var/lib/postgresql/data'],
            'healthcheck': {
                'test': ['CMD', 'pg_isready', '-U', 'airflow'],
                'interval': '5s',
                'retries': 5
            },
            'restart': 'always'
        },
        'redis': {
            'image': 'redis:latest',
            'ports': ['6379:6379'],
            'healthcheck': {
                'test': ['CMD', 'redis-cli', 'ping'],
                'interval': '5s',
                'timeout': '30s',
                'retries': 50
            },
            'restart': 'always'
        },
        'reporting-db': {
            'container_name':
            'reporting-db',
            'image':
            'mongo:latest',
            'env_file': ['.env'],
            'ports': ['27017:27017'],
            'volumes': [
                'reporting-db-volume:/data/db',
                './reporting-db/initdb.d:/docker-entrypoint-initdb.d'
            ],
            'restart':
            'always'
        },
    },
    'volumes': {
        'reporting-db-volume': None
    }
}

result = [{
    'type': 'Ansible',
    'description': {
        'name': 'ensure database is created',
        'postgresql_db': 'name={{dbname}}'
    },
    'path': './test'
}, {
    'type': 'Ansible',
    'description': {
        'name':
        'ensure user has access to database',
        'postgresql_user':
        'db={{dbname}} name={{dbuser}} password={{dbpassword}} priv=ALL'
    },
    'path': './test'
}, {
    'type': 'Ansible',
    'description': {
        'name':
        'Create a new database and user',
        'mongodb_user':
        'login_user=admin login_password={{mongo_admin_pass}} login_port{{mongos_port}} database=test user=admin password={{mongo_admin_pass}} state=present'
    },
    'path': './test'
}]
