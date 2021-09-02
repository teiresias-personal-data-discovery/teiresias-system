import glob, os

from operators.code_analyzer.constants.common import YML_EXTENSIONS
from operators.code_analyzer.constants.context import CONTEXT_MAP
from operators.code_analyzer.utils.analysis.file import parse_YML_file, get_storages
from operators.code_analyzer.utils.analysis.tool import find_tool
from operators.code_analyzer.utils.analysis.context import collect_context, collect_project_context
from operators.code_analyzer.utils.analysis.resolver import resolve_findings
from operators.code_analyzer.utils.analysis.evaluation import evaluate_traces
from operators.code_analyzer.utils.common import flatten


def analyze_code(base_path: str, environment: dict = {}):
    findings = {}
    parsed_files = {}
    yaml_files: list = []
    # tools can be mixed (e.g. Ansible and docker) inside project
    tools = set()

    for root, _, _ in os.walk(base_path):
        # omit non user directories
        if os.path.basename(root).startswith("."):
            continue
        # find all YAML files in the current directory
        yml_patterns = [
            "{}/*.{}".format(root, extension) for extension in YML_EXTENSIONS
        ]
        yml_file_pathes = flatten(
            [glob.glob(pattern) for pattern in yml_patterns])
        yaml_files = [*yaml_files, *yml_file_pathes]
        for yml_file_path in yml_file_pathes:
            parsed_file = parse_YML_file(yml_file_path)
            if parsed_file is None or parsed_file == -1:
                continue
            tool = find_tool(parsed_file)
            if not tool:
                continue
            tools.add(tool)
            parsed_files[yml_file_path] = parsed_file
            traces = get_storages(parsed_file, tool)
            if not traces:
                continue
            path = os.path.relpath(yml_file_path, base_path)
            findings[path] = {"tool": tool, "traces": traces}
            
    yaml_files = [os.path.relpath(yml_file_path, base_path) for yml_file_path in yaml_files]
    if not findings:
        return None, yaml_files

    project_context: dict = collect_project_context(base_path, tools,
                                                    parsed_files)
    resolved = resolve_findings(findings, environment, project_context)
    connection_items = evaluate_traces(resolved, environment)
    return connection_items, yaml_files
