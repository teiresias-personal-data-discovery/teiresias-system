# tool/code dependend context:
#      section_context (e.g. Ansible tasks or docker-compose container) : pattern as regex
#   < project_context (folders & files) : pattern as glob pattern

CONTEXT_MAP: dict = {
    "common": {
        "project_context": {
            '**/.env': 'file',
        },
    },
    "tool_specific": {
        "ansible": {
            "section_context": {
                'hosts': 'key',
                'vars': 'key',
                'vars_files': 'key',
                'vars_prompt': 'key',
                'include_vars': 'key',
                'set_fact': 'key',
                'var': 'key',
            },
            "variables": {
                r"{{ ?(?P<variable>[\w\-]+) ?}}": "variable",
                r"lookup('env', ?'(?P<env_variable>[\w\-]+)')": "variable",
            }
        },
        "docker": {
            "file_context": {
                'secrets': 'key',
            },
            "section_context": {
                "environment": 'key',
                "env_file": 'key',
                "ports": 'key',
            },
            "variables": {
                r"\${(?P<variable>[\w\-]+)(?::~(?P<default_value>[\w\-]*))?}":
                ("variable", "default_value"),
                r"\$(?P<variable>[\w\-]+)":
                "variable"
            }
        }
    }
}
