import os
import json
from mdutils.mdutils import MdUtils
import numpy as np


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
    mdFile = MdUtils(file_name='repositories', title='Repositories')
    sorted(data, key=lambda k: k['type'])
    types = np.unique([d['type'] for d in data])
    mdFile.create_md_file()


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
