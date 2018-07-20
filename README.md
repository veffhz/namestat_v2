## namestat_v2

Lib for advanced work with name statistics in *.py files

##### Prerequisites

Python 3 and pip

##### Install python dependencies

```
pip3 install -r requirements.txt
python3 download_tagger.py
```

##### Usage:

```
python3 namestat.py --size --project_path --source_repo --part_speech --scope --language --output_type
```

* size - top words
* project_path - path to project on filesystem
* source_repo - (url to remote repository (git supported))
* part_speech - type of part of speech (verb or noun)
* scope - scope function (global) or local variables (local)
* language - programming language of project (python supported)
* output_type - show result in console, export in json or csv format

##### Demo:

```
python3 namestat.py -p example_file -ps verb -sc global -o console -l python
```

##### Also you can import functions and usage api (deprecated)

* **get_all_names_in_path(**_path_**,** _language_**)** - get list of all names in files in specified path
* **get_top_functions_names_in_path(**_path_**,** _top_size_**)** - get top function names in files in specified path



##### Testing

python -m unittest test_lib.py