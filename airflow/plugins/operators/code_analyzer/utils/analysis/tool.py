from operators.code_analyzer.constants.common import ANSIBLE_STORAGE_MODULES, DOCKER_HUB_STORAGE_IMAGES
from operators.code_analyzer.constants.common import TOOL_CHARACTERISTICS


def has_mandatory_keys(keys: list, tool: str) -> bool:
    # all mandatory keys should be present
    difference = [
        key for key in TOOL_CHARACTERISTICS[tool]["mandatory_keys"]
        if key not in set(keys)
    ]
    if difference:
        return False
    return True


def find_tool(parsed_file):
    # identify docker-compose mandatory keys at the top level (docker-compose>key)
    if isinstance(parsed_file, dict) and has_mandatory_keys(
            parsed_file.keys(), 'docker'):
        return "docker"
    # identify ansible play mandatory keys at the second level (playbook>play>key)
    if isinstance(parsed_file, list):
        for potential_play in parsed_file:
            if not has_mandatory_keys(potential_play.keys(), 'ansible'):
                return None
        return "ansible"
    return None


def find_Ansible_storage_module(**kwargs):
    key = kwargs.get('key')
    for storage, modules in ANSIBLE_STORAGE_MODULES.items():
        # within Ansible plays, modules can be found as a key
        if key in modules:
            return {"storage": storage}
    return None


def find_Docker_storage_image(**kwargs):
    key = kwargs.get('key')
    candidate = kwargs.get('candidate')
    if key != 'image' or not isinstance(candidate, str):
        return None
    for storage, images in DOCKER_HUB_STORAGE_IMAGES.items():
        # within docker-compose image names followed by ":" are describing the docker image
        if True in [
                candidate.startswith("{}:".format(image)) for image in images
        ]:
            return {"storage": storage}
    return None


map_tool_to_storage_finder = {
    "docker": find_Docker_storage_image,
    "ansible": find_Ansible_storage_module
}
