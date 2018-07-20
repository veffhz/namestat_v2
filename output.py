import json
import csv

from helpers import datetime_name


def process_result(results, _type, output_type):
    if output_type == 'console':
        print_results(results, _type)
    elif output_type == 'json':
        export_to_json(results)
    elif output_type == 'csv':
        export_to_csv(results)


def print_results(results, _type):
    total_part_speech = sum([vb[1] for vb in results])
    print()
    print('total %s %s, %s unique' % (total_part_speech, _type, len(set(results))))

    for item, count in results:
        print("{} : {}".format(item, count))


def export_to_json(results, path='.', file=datetime_name('json')):
    with open('{}/{}'.format(path, file), 'w') as file_handler:
        file_handler.write(json.dumps(dict(results)))


def export_to_csv(results, path='.', file=datetime_name('csv')):
    with open('{}/{}'.format(path, file), "w") as file_handler:
        writer = csv.writer(file_handler, delimiter=',')
        for line in results:
            writer.writerow(line)
