import os
import json
from mdutils.mdutils import MdUtils


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
    #print(os.listdir(root_dir))
    for root, dirs, files in walk_max_depth(root_dir, 2):
        dirs.sort()
        for file in files:
            if file.endswith("metadata.json"):
                metadatafile = os.path.join(cwd, file)
                contents = open(metadatafile)
                metadata = json.load(contents)
                result[root] = (metadatafile, metadata)
    return result


def create_file(files):
    mdFile = MdUtils(file_name='repositories', title='Repositories')


def main():
    """main method."""
    files = find_files()


if __name__ == '__main__':
    main()
