from nltk import pos_tag

from modules import helpers
from modules.code_parsers import get_trees_in_specified_path
from modules.code_parsers import get_local_names_in_tree
from modules.code_parsers import get_functions_in_tree


def word_is_current_type(word, _type):
    tag = pos_tag([word])[0][1]
    if word is None:
        return False
    if _type == 'verb':
        return 'VB' in tag
    elif _type == 'noun':
        return 'NN' in tag


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
