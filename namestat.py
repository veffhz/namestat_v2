import argparse
import helpers

from analyze_handlers import get_top_part_speech
from output import process_result


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--size', help='Top size for get result',
                        type=int, default=10)

    parser.add_argument('-o', '--output_type', choices=['json', 'console', 'csv'],
                        default='console', help='Output mode')

    group_detail = parser.add_argument_group('Detail')
    group_detail.add_argument('-ps', '--part_speech', help='Part of speech',
                              default='verb', nargs='?', choices=['verb', 'noun'])
    group_detail.add_argument('-sc', '--scope', help='Scope of search',
                              default='global', nargs='?', choices=['global', 'local'])
    group_detail.add_argument('-l', '--language', choices=['python'], default='python',
                              help='Programming languages')

    group_source = parser.add_argument_group('Source')
    group_source.add_argument('-p', '--project_path', help='Project path for explore')
    group_source.add_argument('-r', '--source_repo', help='Source project')
    return parser.parse_args()


def main():
    args = parse_args()
    source_repo = args.source_repo
    path_to_repo = args.project_path

    if source_repo is not None and path_to_repo is None:
        path_to_repo = helpers.get_parent_path(source_repo)
        helpers.get_source_repo(source_repo, path_to_repo)

    size = args.size
    scope = args.scope
    part_speech_type = args.part_speech
    language = args.language
    results = get_top_part_speech(path_to_repo, size,
                                  part_speech_type,
                                  scope, language)

    output_type = args.output_type
    process_result(results, part_speech_type, output_type)


if __name__ == "__main__":
    main()
