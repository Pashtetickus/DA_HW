import argparse
import json
import os
import tempfile
from collections import defaultdict

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')


def del_file():
    os.remove(storage_path)


def read_data_file():
    with open(storage_path, 'a+') as f:
        f.seek(0)
        data = f.read()
        if data:
            data = defaultdict(list, json.loads(data))
        else:
            data = defaultdict(list, {})
    return data


def get_value(key):
    data = read_data_file()[key]
    if data is None:
        return ''

    number_of_commas = len(data) - 1
    for value in data:
        if number_of_commas > 0:
            print(value + ', ', end='')
        else:
            print(value)
        number_of_commas -= 1


def write_data(key, val):
    data = read_data_file()
    data[key].append(val)
    with open(storage_path, 'w') as f:
        json.dump(dict(data), f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Enter some keys or values')
    parser.add_argument('--key', type=str, help='key to get values from dict')
    parser.add_argument('--val', type=str, help='value to write to dict')
    parser.add_argument('--del_file', default=False, nargs='?', type=str, help='deleting file storage.data')

    args = parser.parse_args()

    if args.del_file:
        del_file()
    if args.val and not args.key:
        print('You need to provide a key argument')
    elif args.key and not args.val:
        get_value(args.key)
    elif args.val:
        write_data(args.key, args.val)
    else:
        print('None of the argument was provided')
