import os
import json
from mdutils.mdutils import MdUtils
import numpy as np
from itertools import groupby
from operator import itemgetter


def walk_max_depth(top, maxdepth):
    dirs, nondirs = [], []
    for entry in os.scandir(top):
        (dirs if entry.is_dir() else nondirs).append(entry.path)
    yield top, dirs, nondirs
    if maxdepth > 1:
        for path in dirs:
            for x in walk_max_depth(path, maxdepth - 1):
                yield x


def find_files():
    """Return the list of files to process."""
    result = {}
    root_dir = "./repositories"
    cwd = os.getcwd()
    path_separator = os.sep
    #print(os.listdir(root_dir))
    for root, dirs, files in walk_max_depth(root_dir, 2):
        dirs.sort()
        for file in files:
            if file.endswith("metadata.json"):
                metadatafile = os.path.normpath(os.path.join(
                    cwd, file)).replace(path_separator, "/")
                contents = open(metadatafile)
                metadata = json.load(contents)
                result[root] = (metadatafile, metadata)
    return result


def get_data(files):
    data = []
    for key, value in files.items():
        data_dict = {}
        data_dict['type'] = value[1]['type']
        data_dict['name'] = value[1]['name']
        local_path_parts = value[0].split('/')
        repo_name = local_path_parts[-2]
        data_dict[
            'url'] = f'https://github.com/computer-science-engineering/{repo_name}'
        if data_dict['type'] == 'Reading':
            data_dict['reading_sub_header'] = get_reading_sub_header(value[1])
        data.append(data_dict)
    return data


def create_file(files):
    data = get_data(files)
    md_file = MdUtils(file_name='repositories')
    md_file.new_header(level=1, title='Repositories')
    grouped_by_type = groupby(data, key=itemgetter('type'))
    for key, value in grouped_by_type:
        md_file.new_header(level=2, title=key)
        if key == 'Reading':
            write_reading_entries(value, md_file)
        for item in value:
            write_item(item, md_file)
        md_file.new_line()
    md_file.create_md_file()


def write_reading_entries(data, md_file):
    grouped_by_sub_heading = groupby(data,
                                     key=itemgetter('reading_sub_header'))
    for key, value in grouped_by_sub_heading:
        md_file.new_header(level=3, title=key)
        for item in value:
            write_item(item, md_file)


def write_item(item, md_file):
    md_file.new_line(
        '- ' + md_file.new_inline_link(link=item['url'], text=item['name']))


def get_reading_sub_header(file):
    if 'origin' in file and 'name' in file['origin'] and len(
            file['origin']['name']) > 0:
        if 'Notes - ' in file['origin']['name']:
            return file['origin']['name'].replace('Notes - ', '')


def main():
    """main method."""
    files = find_files()
    create_file(files)


if __name__ == '__main__':
    main()
