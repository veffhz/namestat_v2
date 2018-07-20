import ast

import helpers

from namestat import get_functions_in_tree
from namestat import get_trees_in_specified_path


def get_top_py_functions_names_in_path(path, top_size):
    trees = get_trees_in_specified_path(path)
    functions_names = [name for name in helpers.flatten_list([get_functions_in_tree(tree) for tree in trees])
                       if not helpers.is_function_built_in(name)]
    return helpers.most_common(functions_names, top_size)


def get_nodes_names_in_tree(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_all_py_names_in_path(path):
    trees = get_trees_in_specified_path(path)
    names = [name for name in helpers.flatten_list([get_nodes_names_in_tree(tree) for tree in trees])
             if not helpers.is_function_built_in(name)]
    return helpers.flatten_list([helpers.split_case_name(name) for name in names])
