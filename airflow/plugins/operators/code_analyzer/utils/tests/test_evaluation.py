import pytest
from operators.code_analyzer.utils.analysis.evaluation import get_common_storage_environment, evaluate_traces, join_facts
from operators.code_analyzer.utils.tests.mocks.intermediate_results import resolved


@pytest.mark.parametrize("storage, tool, env, environment_occurrance", [
    ('postgres', 'docker', {
        'POSTGRES_USER': 'this--user',
        'POSTGRES_PASSWORD': 'that--pw',
        'POSTGRES_UNSURE': 'TRUE',
    }, {
        'POSTGRES_PASSWORD': 'that--pw',
        'POSTGRES_USER': 'this--user'
    }),
])
def test_get_common_storage_environment(storage, tool, env,
                                        environment_occurrance):
    assert get_common_storage_environment(storage, tool,
                                          env) == environment_occurrance


@pytest.mark.parametrize(
    "traces, environment, storage, storage_modules, tool, joined_facts", [
        ({
            'host': '127.0.0.1',
            'login_user': 'admin',
            'port': "9876"
        }, {
            'POSTGRES_PASSWORD': 'secure'
        }, 'mongodb', ['mongodb_user'], 'ansible', {
            'host': '127.0.0.1',
            'port': '9876',
            'user': 'admin'
        }),
    ])
def test_join_facts(traces, environment, storage, storage_modules, tool,
                    joined_facts):
    assert join_facts(traces, environment, storage, storage_modules,
                      tool) == joined_facts


@pytest.mark.parametrize("resolved, environment, connection_items", [
    (resolved, {}, {
        'postgres-/thesis-analyzeMe.git_2021-05-16_15:38:48/docker-compose.yaml.postgres':
        {
            'values': {
                'port': '5432',
                'user': 'admin',
                'db': 'test'
            },
            'source':
            '/thesis-analyzeMe.git_2021-05-16_15:38:48/docker-compose.yaml',
            'storage_type': 'postgres'
        },
        'reporting-db-/thesis-analyzeMe.git_2021-05-16_15:38:48/docker-compose.yaml.mongodb':
        {
            'values': {},
            'source':
            '/thesis-analyzeMe.git_2021-05-16_15:38:48/docker-compose.yaml',
            'storage_type': 'mongodb'
        },
        'webservers-/thesis-analyzeMe.git_2021-05-16_15:38:48/playbooks/4_pg.yml.postgres':
        {
            'values': {
                'port': '5432',
                'user': 'django',
                'db': 'myapp',
                'password': 'mysupersecretpassword'
            },
            'source':
            '/thesis-analyzeMe.git_2021-05-16_15:38:48/playbooks/4_pg.yml',
            'storage_type': 'postgres'
        }
    }),
])
def test_evaluate_traces(resolved, environment, connection_items):
    assert evaluate_traces(resolved, environment) == connection_items
