## namestat_v2
Lib for collect name statistics in *.py files

##### Prerequisites

Python 3 and pip

##### Install python dependencies

```
pip install -r requirements.txt
python download_tagger.py
```

##### Usage (simple start):

```
python3 namestat.py --size path_to_project
```

##### Demo:

```
python3 namestat.py --size=100 test
```

##### Also you can import functions and usage

* **get_verbs_from_function_name(**_function_name_**)** - get list of verbs in function name

* **get_all_py_names_in_path(**_path_**)** - get list of all names in *.py files in specified path
* **get_top_py_functions_names_in_path(**_path_**,** _top_size_**)** - get top function names in *.py files in specified path
* **get_top__py_functions_verbs_in_path(**_path_**,** _top_size_**)** - get top verbs function names in *.py files in specified path