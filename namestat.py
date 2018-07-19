import re
import ast
import argparse

from nltk import pos_tag

import helpers


def word_is_verb(word):
    tag = pos_tag([word])[0][1]
    return word is not None and re.match(r'V[BDGNPZ]', tag)


def get_trees_in_specified_path(path):
    trees = []
    file_names = helpers.collect_file_names_by_ext(path, '.py')
    for filename in file_names:
        file_content = helpers.get_file_content(filename)
        try:
            trees.append(ast.parse(file_content))
        except SyntaxError:
            pass
    return trees


def get_nodes_names_in_tree(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def get_functions_names_in_tree(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def get_verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if word_is_verb(word)]


def get_names_on_function_handle_to_path(path, func):
    trees = get_trees_in_specified_path(path)
    return [name for name in helpers.flatten_list([func(tree) for tree in trees])
            if not helpers.is_function_built_in(name)]


def get_all_py_names_in_path(path):
    names = get_names_on_function_handle_to_path(path, get_nodes_names_in_tree)
    return helpers.flatten_list([helpers.split_case_name(name) for name in names])


def get_top_py_functions_verbs_in_path(path, top_size):
    functions_names = get_names_on_function_handle_to_path(path, get_functions_names_in_tree)
    verbs = helpers.flatten_list([get_verbs_from_function_name(name) for name in functions_names])
    return helpers.most_common(verbs, top_size)


def get_top_py_functions_names_in_path(path, top_size):
    functions_names = get_names_on_function_handle_to_path(path, get_functions_names_in_tree)
    return helpers.most_common(functions_names, top_size)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', help='Top size for get verbs', type=int, default=200)
    required_source = parser.add_mutually_exclusive_group(required=True)
    required_source.add_argument('-p', '--project_path', help='Project path for explore')
    required_source.add_argument('-r', '--source_repo', help='Source project')
    return parser.parse_args()


if __name__ == "__main__":

    args = parse_args()
    source_repo = args.source_repo
    path_to_repo = args.project_path

    if source_repo is not None and path_to_repo is None:
        path_to_repo = helpers.get_parent_path(source_repo)
        helpers.get_source_repo(source_repo, path_to_repo)

    result_verbs = get_top_py_functions_verbs_in_path(path_to_repo, args.size)

    total_verbs = sum([vb[1] for vb in result_verbs])
    print('total %s verbs, %s unique' % (total_verbs, len(set(result_verbs))))

    for _verb, _occurence in helpers.most_common(result_verbs, args.size):
        print(_verb, _occurence)
