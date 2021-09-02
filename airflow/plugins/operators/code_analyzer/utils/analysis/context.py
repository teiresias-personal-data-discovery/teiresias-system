import glob, os

from operators.code_analyzer.constants.context import CONTEXT_MAP
from operators.code_analyzer.utils.common import get_intersection, flatten, unpack, findall_regex


def get_tool_and_common_context_map(tools, context_type: str) -> dict:
    context_map: dict = {}
    for tool in tools:
        context_map = {
            **context_map,
            **CONTEXT_MAP.get("tool_specific", {}).get(tool, {}).get(
                context_type, {})
        }
    common_context_domains = [
        context_domain for context_domain in list(CONTEXT_MAP)
        if context_domain != "tool_specific"
    ]
    for context_domain in common_context_domains:
        context_map = {
            **context_map,
            **CONTEXT_MAP.get(context_domain, {}).get(context_type, {})
        }
    return context_map


def get_context_of_dictionary(entity: dict, context_pattern: str,
                              candidate_type: str) -> dict:
    findings: dict = {}
    for key, value in entity.items():
        if candidate_type == 'key':
            pattern_match = findall_regex(context_pattern, key)
            if len(pattern_match) == 1:
                unpacked = unpack(value, key)
                findings = {**findings, **unpacked}
    return findings


def collect_context(entity, tool: str, context_type: str) -> dict:
    context_map = get_tool_and_common_context_map([tool], context_type)
    findings: dict = {}
    for context_pattern, candidate in context_map.items():
        if isinstance(entity, dict):
            findings = {
                **findings,
                **get_context_of_dictionary(entity, context_pattern, candidate)
            }
        if isinstance(entity, list):
            for section in entity:
                if not isinstance(section, dict):
                    continue
                findings = {
                    **findings,
                    **get_context_of_dictionary(section, context_pattern, candidate)
                }
    return findings


def collect_project_context(base_path: str, tools: set,
                            parsed_files: dict) -> dict:
    project_context_map = get_tool_and_common_context_map(
        tools, 'project_context')
    patterns_with_path = [
        "{}/{}".format(base_path, pattern)
        for pattern in project_context_map.keys()
    ]
    file_pathes = flatten(
        [glob.glob(pattern, recursive=True) for pattern in patterns_with_path])
    findings: dict = {}
    for path in file_pathes:
        parsed_file = parsed_files.get(path)
        if parsed_file is None:
            continue
        if isinstance(parsed_file, dict):
            for key, value in parsed_file.items():
                unpacked = unpack(value, key)
                findings = {**findings, **unpacked}
        # assumption: project context is not deep nested
        if isinstance(parsed_file, list):
            for section in parsed_file:
                if not isinstance(section, dict):
                    continue
                for key, value in section.items():
                    unpacked = unpack(value, key)
                    findings = {**findings, **unpacked}
    return findings
