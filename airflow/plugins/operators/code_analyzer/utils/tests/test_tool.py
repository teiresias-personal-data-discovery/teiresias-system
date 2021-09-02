import pytest

from operators.code_analyzer.utils.analysis.tool import find_tool, has_mandatory_keys
from operators.code_analyzer.utils.tests.mocks.parsed_YAML import parsed_playbook_yaml_postgres, parsed_playbook_yaml_mongodb, parsed_playbook_yaml_mongodb_postgres, parsed_docker_compose_mongodb_postgres


@pytest.mark.parametrize(
    "keys, tool, has_character",
    [(["hosts", "user", "roles", "become"], 'ansible', True),
     (["user", "roles", "become"], 'ansible', False),
     (["version", "services", "volumes"], 'docker', True),
     (["version", "services", "volumes"], 'ansible', False),
     (["version", "something"], 'docker', False)])
def test_has_mandatory_keys(keys, tool, has_character):
    assert has_mandatory_keys(keys, tool) == has_character


@pytest.mark.parametrize("parsed_file, tool", [
    (parsed_playbook_yaml_postgres, 'ansible'),
    (parsed_playbook_yaml_mongodb, 'ansible'),
    (parsed_playbook_yaml_mongodb_postgres, 'ansible'),
    (parsed_docker_compose_mongodb_postgres, 'docker'),
    ({
        "version": "humphrey bogart",
        "hosts": [""]
    }, None),
])
def test_find_tool(parsed_file, tool):
    assert find_tool(parsed_file) == tool
