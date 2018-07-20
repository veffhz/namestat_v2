import ast

import helpers
from namestat import get_names_on_function_handle_to_path
from namestat import get_functions_names_in_tree


def get_top_py_functions_names_in_path(path, top_size):
    functions_names = get_names_on_function_handle_to_path(path, get_functions_names_in_tree)
    return helpers.most_common(functions_names, top_size)


def get_nodes_names_in_tree(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_all_py_names_in_path(path):
    names = get_names_on_function_handle_to_path(path, get_nodes_names_in_tree)
    return helpers.flatten_list([helpers.split_case_name(name) for name in names])