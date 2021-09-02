from operators.code_analyzer.constants.common import STORAGE_CHARACTERISTICS
from operators.code_analyzer.utils.common import get_intersection


def get_common_storage_environment(storage: str, tool: str, env: dict) -> dict:
    lookup = STORAGE_CHARACTERISTICS.get(tool, {}).get(storage,
                                                       {}).get('env', {})
    environment_occurrance = get_intersection(list(lookup), list(env))
    return {key: env.get(key, {}) for key in environment_occurrance}


def join_facts(traces: dict, environment: dict, storage: str,
               storage_modules: str, tool: str) -> dict:
    values: dict = {}
    for module in storage_modules:
        storage_map = STORAGE_CHARACTERISTICS.get(tool, {}).get(module, {})
        values = {
            **storage_map.get('defaults', {}),
            **{
                key: value
                for key, value in traces.items() if key in list(
                    storage_map.get('env', {}).values())
            }
        }
        for internal_key, abstract_key in storage_map.get('env', {}).items():
            trace = traces.get(internal_key, environment.get(internal_key))
            if trace:
                values = {**values, abstract_key: trace}
    return values


def evaluate_traces(resolved: dict, environment: dict):
    connection_items: dict = {}
    for path, finding in resolved.items():
        for (tool, storage, node_title), resolved_traces in finding.items():
            storage_modules = resolved_traces.get("storage_modules", [])
            environment_occurrance = get_common_storage_environment(
                storage, tool, environment)
            values = join_facts(resolved_traces, environment_occurrance,
                                storage, storage_modules, tool)
            # omit leading $ since mongo does not accept it as key
            current_node_title = node_title
            while current_node_title.startswith("$"):
                current_node_title = current_node_title[1:]

            storage_identifier = "{}.{}".format(current_node_title, storage)
            connection_items = {
                **connection_items, storage_identifier: {
                    'values': values,
                    'source': path,
                    'storage_type': storage
                }
            }
    return connection_items
