import re
import ast
import argparse

from nltk import pos_tag

import helpers


def word_is_current_type(word, _type):
    tag = pos_tag([word])[0][1]
    if word is None:
        return False
    if _type == 'verb':
        return re.match(r'V[BDGNPZ]', tag)
    elif _type == 'noun':
        return re.match(r'NN', tag)


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


def get_functions_names_in_tree(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def get_part_speech_from_function_name(function_name, _type):
    return [word for word in function_name.split('_') if word_is_current_type(word, _type)]


def get_names_on_function_handle_to_path(path, func):
    trees = get_trees_in_specified_path(path)
    return [name for name in helpers.flatten_list([func(tree) for tree in trees])
            if not helpers.is_function_built_in(name)]


def get_top_functions_part_speech(path, top_size, _type):
    functions_names = get_names_on_function_handle_to_path(path, get_functions_names_in_tree)
    verbs = helpers.flatten_list([get_part_speech_from_function_name(name, _type) for name in functions_names])
    return helpers.most_common(verbs, top_size)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', help='Top size for get result', type=int, default=200)
    parser.add_argument('-ps', '--part_speech', help='Part of speech',
                        default='verb', nargs='?', choices=['verb', 'noun'])
    parser.add_argument('-sc', '--scope', help='Scope of search',
                        default='global', nargs='?', choices=['global', 'local'])
    required_source = parser.add_mutually_exclusive_group(required=True)
    required_source.add_argument('-p', '--project_path', help='Project path for explore')
    required_source.add_argument('-r', '--source_repo', help='Source project')
    return parser.parse_args()


def print_results(results, _type, size):
    total_part_speech = sum([vb[1] for vb in results])
    print('total %s %s, %s unique' % (total_part_speech, _type, len(set(results))))

    for part_speech, occurence in helpers.most_common(results, size):
        print(part_speech, occurence)


def main():
    args = parse_args()
    source_repo = args.source_repo
    path_to_repo = args.project_path

    if source_repo is not None and path_to_repo is None:
        path_to_repo = helpers.get_parent_path(source_repo)
        helpers.get_source_repo(source_repo, path_to_repo)

    size = args.size
    _type = args.part_speech
    results = get_top_functions_part_speech(path_to_repo, size, _type)
    print_results(results, _type, size)


if __name__ == "__main__":
    main()
