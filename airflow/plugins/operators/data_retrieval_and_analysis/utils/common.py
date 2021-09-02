import re

from operators.data_retrieval_and_analysis.constants.lookup import personal_data_value_patterns, personal_data_key_words
from operators.data_retrieval_and_analysis.utils.nlp import process_proximity

storage_map = {"mongo": lambda info: "mongodb+srv" if info.get('uri_option') == 'srv' else "mongodb", "postgre": lambda info: "postgresql"}
mandatory_default_port = {"postgre": "5432"}


def get_uri(storage: dict, type) -> str:
    port = storage.get('port') if storage.get(
        'port') is not None else mandatory_default_port.get(type)
    if port is not None:
        return "{}://{}:{}@{}:{}/{}".format(
            storage_map.get(type, lambda i: '')(storage),
            *[storage.get(key) for key in [
                'user',
                'password',
                'host',
            ]], port, storage.get('db'))
    return "{}://{}:{}@{}/{}".format(
        storage_map.get(type, lambda i: '')(storage),
        *[storage.get(key) for key in [
            'user',
            'password',
            'host',
            'db',
        ]])


def get_serializable_sqlalchemy_type(type_class):
    try:
        return type_class.__class__.__name__
    except:
        return 'unknown'


def get_list_from_tuple(obj):
    try:
        return [item for item in obj]
    except:
        return obj


def findall_regex(regex_str: str, candidate: str) -> list:
    iterator = re.finditer(regex_str, candidate)
    occurrance = []
    for match in iterator:
        occurrance.append((match.groupdict() or {
            "hit": regex_str
        }, (match.start(), match.end())))
    return occurrance


def analyze_key(key):
    proximities = [
        get_list_from_tuple(proximity)
        for proximity in process_proximity(key, personal_data_key_words)
    ]
    if proximities:
        return [{"candidate": key, "proximity": proximities, "type": "key"}]
    return []


def analyze_value(value):
    matches = []
    if isinstance(value, str):
        for pattern_name, pattern in personal_data_value_patterns.items():
            match = findall_regex(pattern, value)
            if match:
                matches = [
                    *matches, {
                        "candidate": value,
                        "pattern": pattern_name,
                        "type": "value"
                    }
                ]
    return matches


def analyze_json(data):
    findings = []
    if isinstance(data, dict):
        for key, value in data.items():
            findings.extend(analyze_key(key))
            findings.extend(analyze_json(value))
    elif isinstance(data, list):
        for item in data:
            findings.extend(analyze_json(item))
    else:
        findings.extend(analyze_value(data))
    return findings
