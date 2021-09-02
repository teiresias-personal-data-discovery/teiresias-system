import pytest

from operators.code_analyzer.constants.context import CONTEXT_MAP
from operators.code_analyzer.utils.analysis.resolver import resolve_string, replace_variables_with_values, resolve_findings, resolve_match, resolve_match_multiple
from operators.code_analyzer.utils.tests.mocks.parsed_environment import ENV
from operators.code_analyzer.utils.tests.mocks.parsed_YAML import parsed_docker_compose_mongodb_postgres, parsed_playbook_yaml_mongodb_postgres
from operators.code_analyzer.utils.tests.mocks.intermediate_results import findings, resolved


@pytest.mark.parametrize("candidate, patterns, resolved_variables, result", [
    (parsed_docker_compose_mongodb_postgres.get('services', {}).get(
        'postgres', {}).get("environment").get('POSTGRES_DB'),
     CONTEXT_MAP.get("tool_specific", {}).get('docker', {}).get(
         "variables", {}), {
             "db": "db1234"
         }, ([{
             'variable': 'db',
             'value': 'db1234',
             'default_value': 'dags',
             'span': (0, 11)
         }], [])),
    (parsed_docker_compose_mongodb_postgres.get('services', {}).get(
        'postgres', {}).get("environment").get('POSTGRES_USER'),
     CONTEXT_MAP.get("tool_specific", {}).get('docker', {}).get(
         "variables", {}), {
             "db": "db1234"
         }, ([], [])),
    (parsed_playbook_yaml_mongodb_postgres[1].get(
        'tasks', {})[1].get('postgresql_user'),
     CONTEXT_MAP.get("tool_specific", {}).get('ansible', {}).get(
         "variables", {}), {
             "dbname": 'user_store',
             "dbuser": 'Bert'
         }, ([{
             'variable': 'dbname',
             'value': 'user_store',
             'default_value': None,
             'span': (3, 13),
         }, {
             'variable': 'dbuser',
             'value': 'Bert',
             'default_value': None,
             'span': (19, 29)
         }], [{
             'span': (39, 53),
             'variable': 'dbpassword'
         }])),
])
def test_resolve_string(candidate, patterns, resolved_variables, result):
    assert resolve_string(candidate, patterns, resolved_variables) == result


@pytest.mark.parametrize("candidate, resolver_stack,new_candidate", [
    ('db={{dbname}} name={{dbuser}} password={{dbpassword}} priv=ALL',
     [{
         'variable': 'dbname',
         'value': 'a1',
         'span': (3, 13),
     }, {
         'variable': 'dbpassword',
         'value': 'p1',
         'span': (39, 53)
     }, {
         'variable': 'dbuser',
         'value': 'Bert',
         'span': (19, 29)
     }], 'db=a1 name=Bert password=p1 priv=ALL'),
])
def test_replace_variables_with_values(candidate, resolver_stack,
                                       new_candidate):
    assert replace_variables_with_values(candidate,
                                         resolver_stack) == new_candidate


@pytest.mark.parametrize(
    "match, patterns, facts, resolved", [({
        'POSTGRES_USER': '${user_name}'
    }, {
        '\\${(?P<variable>[\\w\\-]+)(?::~(?P<default_value>[\\w\\-]*))?}':
        ('variable', 'default_value'),
        '\\$(?P<variable>[\\w\\-]+)':
        'variable'
    }, {
        'user_name': 'Asterix',
    }, {
        'POSTGRES_USER': 'Asterix'
    }), ({
        'POSTGRES_USER': '${user_name}'
    }, {}, {
        'user_name': 'Asterix',
    }, {})])
def test_resolve_match(match, patterns, facts, resolved):
    assert resolve_match(match, patterns, facts) == resolved


@pytest.mark.parametrize("match, patterns, facts, resolved", [
    ({
        'POSTGRES_USER': '${user_name}'
    }, {
        '\\${(?P<variable>[\\w\\-]+)(?::~(?P<default_value>[\\w\\-]*))?}':
        ('variable', 'default_value'),
        '\\$(?P<variable>[\\w\\-]+)':
        'variable'
    }, {
        'user_name': '${admin}',
        'admin': 'Asterix',
    }, {
        'POSTGRES_USER': 'Asterix'
    }),
])
def test_resolve_match_multiple(match, patterns, facts, resolved):
    assert resolve_match_multiple(match, patterns, facts) == resolved


@pytest.mark.parametrize("findings, environment, project_context, resolved",
                         [(findings, {
                             'mongos_port': '88088',
                             'webservers': '1234.6543.9876'
                         }, {}, resolved)])
def test_resolve_findings(findings, environment, project_context, resolved):
    assert resolve_findings(findings, environment, project_context) == resolved
