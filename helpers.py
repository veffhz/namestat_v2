import os
import re
import collections
import time

from os.path import abspath

from git import Repo


def flatten_list(_list):
    return sum([list(item) for item in _list], [])


def most_common(names, top_size):
    return collections.Counter(names).most_common(top_size)


def collect_file_names_by_ext(path, file_ext):
    file_names = []
    for dir_name, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith(file_ext):
                file_names.append(os.path.join(dir_name, file))
    return file_names


def get_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as attempt_handler:
        return attempt_handler.read()


def is_function_built_in(name):
    return name.startswith('__') and name.endswith('__')


def split_case_name(string_to_split):
    return [name for name in string_to_split.split('_') if name]


def get_parent_path(source_repo):
    name = re.search(r'^.*/(.*).git$', source_repo)
    return abspath('../{}'.format(name.group(1)))


def get_source_repo(source_repo, path_to_repo, type_repo='git'):
    if type_repo == 'git':
        Repo.clone_from(source_repo, path_to_repo)


def datetime_name(ext):
    return time.strftime("%Y%m%d-%H%M%S.{}".format(ext))
