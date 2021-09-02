import re
from collections.abc import Callable
import copy

from operators.code_analyzer.utils.analysis.context import get_tool_and_common_context_map
from operators.code_analyzer.utils.common import findall_regex, tokenize_by_whitespace


def replace_variables_with_values(candidate: str, resolver_stack: list) -> str:
    new_candidate = candidate
    desc_sorted_resolver = sorted(resolver_stack,
                                  key=lambda elem: elem.get("span")[1],
                                  reverse=True)
    for resolver in desc_sorted_resolver:
        (start, end) = resolver.get('span', ())
        new_candidate = "{}{}{}".format(new_candidate[:start],
                                        resolver.get('value', ''),
                                        new_candidate[end:])
    return new_candidate


def resolve_string(candidate: str, patterns: dict,
                   context: dict):
    resolved = []
    unresolved = []
    for pattern, _ in patterns.items():
        variables = findall_regex(pattern, candidate)
        for (variable_dict, span) in variables:
            variable = variable_dict.get("variable")
            default_value = variable_dict.get("default_value")
            resolved_value = context.get(variable)
            if (resolved_value is not None
                    and resolved_value != '') or default_value is not None:
                resolved.append({
                    'variable': variable,
                    "value": resolved_value,
                    "default_value": default_value,
                    "span": span
                })
            else:
                unresolved.append({'variable': variable, "span": span})
    return resolved, unresolved


def resolve_match(match: dict, patterns: dict, context: dict) -> dict:
    resolved_match: dict = {}
    unresolved_match: dict = {}
    for key, value in match.items():
        if not isinstance(value, str):
            unresolved_match = {**unresolved_match, **{key: value}}
            continue
        resolved, unresolved = resolve_string(value, patterns, context)
        new_value = replace_variables_with_values(value, resolved)
        if new_value != value:
            tokens = tokenize_by_whitespace(new_value)
            resolved_match = {
                **resolved_match, key: {
                    **resolved_match.get(key, {}),
                    **tokens
                } if isinstance(tokens, dict) else tokens
            }
        for item in unresolved:
            unresolved_match = {**unresolved_match, **{key: item}}
    return resolved_match


def resolve_match_multiple(match: dict, patterns: dict, context: dict) -> dict:
    string_variables_keys = []
    string_variables = match.get("string_variables")
    if string_variables is not None:
        temp_string_variables: dict = {}
        for index, string_variable in enumerate(string_variables):
            string_variables_keys.append(index)
            temp_string_variables = {
                **temp_string_variables, index: string_variable
            }
        current_resolved_match: dict = {
            **{
                key: value
                for key, value in match.items() if key != "string_variables"
            },
            **temp_string_variables
        }
    else:
        current_resolved_match = match
    preserved_match = {}
    while (current_resolved_match):
        current_resolved_match = resolve_match(current_resolved_match,
                                               patterns, context)
        if current_resolved_match:
            preserved_match = current_resolved_match
    unpacked = {
        key: value
        for key, value in preserved_match.items()
        if key not in string_variables_keys
    }
    for key in string_variables_keys:
        unpacked = {**unpacked, **preserved_match.get(key, {})}
    return unpacked


def resolve_findings(findings: dict, environment: dict,
                     project_context: dict) -> dict:
    resolved: dict = {}
    global_context: dict = {**project_context, **environment}
    for path, file in findings.items():
        file_resolving: dict = {}
        tool = file.get("tool")
        patterns = get_tool_and_common_context_map([tool], 'variables')
        for node_name, trace in file.get("traces", {}).items():
            storage = trace.get('match', {}).get('storage')
            storage_modules = trace.get('match', {}).get('storage_modules')
            result = resolve_match_multiple(trace.get(
                'env_variables', {}), patterns, {
                    **trace.get('env_variables', {}),
                    **global_context
                })
            file_resolving = {
                **file_resolving, (tool, storage, node_name): {
                    "storage_modules": storage_modules,
                    **trace.get('env_variables', {}),
                    **result
                }
            }
        resolved = {**resolved, path: file_resolving}
    return resolved
