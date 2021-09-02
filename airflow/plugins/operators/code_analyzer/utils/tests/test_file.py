import pytest

from operators.code_analyzer.utils.analysis.file import get_storages, traverse_section_map
from operators.code_analyzer.utils.tests.mocks.parsed_YAML import parsed_playbook_yaml_postgres, parsed_playbook_yaml_mongodb, parsed_playbook_yaml_mongodb_postgres, parsed_docker_compose_mongodb_postgres
from operators.code_analyzer.constants.common import TOOL_CHARACTERISTICS, DEPENDENCY_MAP


@pytest.mark.parametrize("map, entity, tool, current_candidate_node_name, findings", [
    (TOOL_CHARACTERISTICS.get('ansible', {}).get(
        'section_map'
    ), parsed_playbook_yaml_postgres, 'ansible', None, {
        'webservers':
        {
            'env_variables':
            {
                'string_variables':
                [
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
                'storage_modules': ['postgresql_user'],
                'storage': 'postgres'
            }
        }
    }),
    (TOOL_CHARACTERISTICS.get('ansible', {}).get(
        'section_map'
    ), parsed_playbook_yaml_mongodb_postgres, 'ansible', None, {
        'RDB1':
        {
            'env_variables':
            {
                'string_variables': [
                    'db={{dbname}} name={{dbuser}} password={{dbpassword}} priv=ALL'
                ],
                'dbname':
                'myapp',
                'dbuser':
                'django',
                'dbpassword':
                'mysupersecretpassword'
            },
            'match': {
                'storage_modules': ['postgresql_user'],
                'storage': 'postgres'
            }
        },
        'data':
        {
            'env_variables': {
                'string_variables': [
                    'login_user=admin login_password={{mongo_admin_pass}} login_port={{mongos_port}} database=test user=admin password={{mongo_admin_pass}} state=present'
                ],
                'dbname':
                'user_collections',
                'login_user':
                'nosqler',
                'mongo_admin_pass':
                'wysiwyg'
            },
            'match': {
                'storage_modules': ['mongodb_user'],
                'storage': 'mongodb'
            }
        }
    }),
    (TOOL_CHARACTERISTICS.get('docker', {}).get('section_map'),
     parsed_docker_compose_mongodb_postgres, 'docker', None, {
         'postgres': {
             'env_variables': {
                 'port': '5432',
                 'POSTGRES_USER': 'admin',
                 'POSTGRES_DB': '${db:~dags}',
                 'use_env_files': ['.env']
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
     }),
])
def test_traverse_section_map(map, entity, tool, current_candidate_node_name,
                              findings):
    assert traverse_section_map(map, entity, tool,
                                current_candidate_node_name) == findings


@pytest.mark.parametrize("entity, tool, findings", [
    (parsed_docker_compose_mongodb_postgres, 'docker', {
        'postgres': {
            'env_variables': {
                'port': '5432',
                'POSTGRES_USER': 'admin',
                'POSTGRES_DB': '${db:~dags}',
                'use_env_files': ['.env']
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
    }),
    (parsed_playbook_yaml_postgres, 'ansible', {
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
                'storage_modules': ['postgresql_user'],
                'storage': 'postgres'
            }
        }
    }),
])
def test_get_storages(entity, tool, findings):
    assert get_storages(entity, tool) == findings
