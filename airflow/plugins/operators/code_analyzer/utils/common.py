import re


def flatten(list_of_lists: list) -> list:
    return [x for y in list_of_lists for x in y]


def get_intersection(a: list, b: list) -> list:
    return [x for x in a if x in b]


def get_difference(a: list, b: list) -> list:
    return [x for x in a if x not in b]


def unpack(item: dict, parent):
    unpacked: dict = {}
    if isinstance(item, str) or isinstance(item, list):
        return {parent: item} if parent else item
    if isinstance(item, dict):
        for key, value in item.items():
            unpacked = {
                **unpacked,
                **{
                    key: value
                }
            } if isinstance(value, str) else {
                **unpacked,
                **unpack(value, key)
            }

    return unpacked


def findall_regex(regex_str: str, candidate: str) -> list:
    iterator = re.finditer(regex_str, candidate)
    occurrance = []
    for match in iterator:
        occurrance.append((match.groupdict() or {
            "hit": regex_str
        }, (match.start(), match.end())))
    return occurrance


def tokenize_by_whitespace(string: str):
    if string == "":
        return ""
    try:
        assignments = [token for token in string.split(" ") if token != '']
        separated_assignments = [
            assignment.split("=") for assignment in assignments
        ]
        return {key: value for [key, value] in separated_assignments}
    except:
        return string
