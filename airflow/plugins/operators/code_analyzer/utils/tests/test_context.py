import pytest
import glob
from operators.code_analyzer.utils.analysis.context import get_context_of_dictionary, collect_project_context, collect_context
from operators.code_analyzer.utils.tests.mocks.parsed_YAML import parsed_playbook_yaml_postgres, parsed_playbook_yaml_mongodb, parsed_playbook_yaml_mongodb_postgres, parsed_docker_compose_mongodb_postgres


def test_collect_project_context(monkeypatch):
    def mockreturn(context_pattern, **recursive):
        if context_pattern == '/**/*_vars/**':
            return ['/variables/group_vars/1/']
        if context_pattern == '/**/.env':
            return ['/.env']
        if context_pattern == '/**/roles/**/vars/**':
            return ['/utils/roles/ec2/vars/gateway']
        return []

    monkeypatch.setattr(glob, 'glob', mockreturn)

    assert {} == collect_project_context(
        '', {'ansible', 'docker'},
        {'path/to/heaven/playbooks': {
            'test': 'lets play'
        }})

    assert {
        'variable1': 'one',
        'variable2': 'two',
        'variable3': 'three'
    } == collect_project_context('', {'ansible', 'docker'}, {
        '/utils/roles/ec2/vars/gateway': {
            'variable1': 'one'
        },
        "/variables/group_vars/1/": [{
            'variable2': 'two'
        }, {
            'variable3': 'three'
        }],
        "/home/": {
            'variable4': 'four'
        }
    })
