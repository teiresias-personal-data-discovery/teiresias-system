from ruamel.yaml import YAML
from pathlib import Path
from mergedeep import merge

from operators.code_analyzer.utils.analysis.tool import map_tool_to_storage_finder
from operators.code_analyzer.utils.analysis.context import collect_context
from operators.code_analyzer.constants.common import TOOL_CHARACTERISTICS


def parse_YML_file(file_path: str):
    with Path(file_path) as path:
        try:
            yaml = YAML(typ='safe')
            return yaml.load(path)
        except:
            return -1


def traverse_section_map(map, entity, tool, current_candidate_node_name):
    findings: dict = {}
    new_current_candidate_node_name = current_candidate_node_name
    if isinstance(entity, dict):
        for map_key, map_value in map.items():
            if map_key == "candidates_node_names":
                # handle each potential candidate branch recursively
                for candidate_node_name, candidate_entity in entity.items():
                    new_current_candidate_node_name = candidate_node_name
                    findings = {
                        **findings,
                        **traverse_section_map(
                            map_value, candidate_entity, tool, new_current_candidate_node_name)
                    }
            elif new_current_candidate_node_name is None and map_key not in entity:
                # early stop if no match on map
                return {}
            elif map_value == "candidate_node_name":
                # preserve node name of potential storage
                new_current_candidate_node_name = entity.get(map_key)
            elif callable(map_value) and entity.get(map_key):
                # call candidate handler from map with corresponding value from entity
                try:
                    candidate_handler_return = map_value(entity.get(map_key))
                    findings = {
                        **findings, new_current_candidate_node_name:
                        merge({},
                              findings.get(new_current_candidate_node_name,
                                           {}), candidate_handler_return)
                    }
                except Exception as e:
                    print('Error', e)
            elif not callable(map_value):
                # traverse map and entity simultaneously
                findings = {
                    **findings,
                    **traverse_section_map(map_value, entity.get(map_key, {}), tool, new_current_candidate_node_name)
                }

    if isinstance(entity, list):
        for item in entity:
            findings = {
                **findings,
                **traverse_section_map(map, item, tool, new_current_candidate_node_name)
            }
    # omit unmatched traces
    return {
        node: traces
        for node, traces in findings.items() if "match" in traces.keys()
    }


def get_storages(entity, tool: str) -> list:
    section_map = TOOL_CHARACTERISTICS.get(tool, {}).get('section_map', [])
    return traverse_section_map(section_map, entity, tool, None)
