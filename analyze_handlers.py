import re
import ast

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


def get_extention(language):
    if language == 'python':
        return '.py'


def get_trees_in_specified_path(path, language):
    trees = []
    ext = get_extention(language)
    file_names = helpers.collect_file_names_by_ext(path, ext)
    for filename in file_names:
        file_content = helpers.get_file_content(filename)
        try:
            trees.append(ast.parse(file_content))
        except SyntaxError:
            pass
    return trees


def get_functions_in_tree(tree, is_body=False):
    if not is_body:
        return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    else:
        return [node.body for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def get_local_names_in_tree(tree):
    functions = get_functions_in_tree(tree, is_body=True)
    names = [[a.targets[0].id for a in name if isinstance(a, ast.Assign)] for name in functions]
    return names


def get_part_speech_from_function_name(function_name, _type):
    return [word for word in function_name.split('_') if word_is_current_type(word, _type)]


def get_top_part_speech_in_local(trees):
    part_speech_names = [name for name in helpers.flatten_list([get_local_names_in_tree(tree) for tree in trees])]
    return helpers.flatten_list([name for name in part_speech_names])


def get_top_part_speech_in_global(_type, trees):
    part_speech_names = [name for name in helpers.flatten_list([get_functions_in_tree(tree) for tree in trees])
                         if not helpers.is_function_built_in(name)]
    return helpers.flatten_list([get_part_speech_from_function_name(name, _type)
                                 for name in part_speech_names])


def get_top_part_speech(path, top_size, _type, scope, language):

    trees = get_trees_in_specified_path(path, language)

    results = {'global': get_top_part_speech_in_global(_type, trees),
               'local': get_top_part_speech_in_local(trees)}

    return helpers.most_common(results[scope], top_size)
