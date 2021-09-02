import pytest

from operators.code_analyzer.utils.common import unpack, findall_regex, tokenize_by_whitespace
from operators.code_analyzer.constants.context import CONTEXT_MAP


@pytest.mark.parametrize("value, parent, unpacked", [({
    'environment': {
        'SUPER_PWD': 'qwertz',
        'SUPER_USER': 'admin'
    }
}, None, {
    'SUPER_PWD': 'qwertz',
    'SUPER_USER': 'admin'
}),
                                                     ({
                                                         'SUPER_PWD': 'qwertz',
                                                         'SUPER_USER': 'admin'
                                                     }, None, {
                                                         'SUPER_PWD': 'qwertz',
                                                         'SUPER_USER': 'admin'
                                                     }),
                                                     ('webservers', 'hosts', {
                                                         'hosts': 'webservers'
                                                     })])
def test_unpack(value, parent, unpacked):
    assert unpack(value, parent) == unpacked


@pytest.mark.parametrize("regex_str, candidate, result", [
    (list(
        CONTEXT_MAP.get("tool_specific", {}).get("docker", {}).get(
            "variables", {}))[0], '${variable__name}', [({
                'variable': 'variable__name',
                'default_value': None
            }, (0, 17))]),
    (list(
        CONTEXT_MAP.get("tool_specific", {}).get("docker", {}).get(
            "variables", {}))[0], '${VARIABLE__NAME:~with-defaultValue}...', [
                ({
                    'variable': 'VARIABLE__NAME',
                    'default_value': 'with-defaultValue'
                }, (0, 36))
            ]),
    (list(
        CONTEXT_MAP.get("tool_specific", {}).get("ansible", {}).get(
            "variables", {}))[0], '...{{ jinja }}', [({
                'variable': 'jinja'
            }, (3, 14))]),
    (list(
        CONTEXT_MAP.get("tool_specific", {}).get("ansible", {}).get(
            "variables", {}))[0], '$jinja', []),
    (list(
        CONTEXT_MAP.get("tool_specific", {}).get("ansible", {}).get(
            "section_context", {}))[5], 'set_fact__set_fact', [({
                'hit':
                'set_fact'
            }, (0, 8)), ({
                'hit': 'set_fact'
            }, (10, 18))]),
])
def test_findall_regex(regex_str, candidate, result):
    assert findall_regex(regex_str, candidate) == result


@pytest.mark.parametrize("string, tokens", [
    ("", ""),
    ("test", 'test'),
    ("one=1 three=${3}", {
        'one': '1',
        'three': '${3}'
    }),
])
def test_tokenize(string, tokens):
    assert tokenize_by_whitespace(string) == tokens
