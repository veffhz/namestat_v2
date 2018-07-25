import ast
from modules import helpers


def get_extention(language):
    languages = {'python': '.py'}
    return languages[language]


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
