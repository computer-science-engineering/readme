from mimetypes import init
import os
from reprlib import recursive_repr
import stat
import git
import json
import shutil


def get_repo_list(file):
    with open(file, 'r') as json_file:
        data = json.load(json_file)
    return data


def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clean_repositories_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir, onerror=remove_readonly)
    os.makedirs(dir)


# git config --system core.longpaths true
def clone_repositories(list):
    parent_folder = './repositories'
    clean_repositories_dir(parent_folder)
    for item in list:
        folder_name = get_folder_name(item['url'])
        local_path = os.path.join(parent_folder, folder_name)
        git.Repo.clone_from(item['url'], local_path)
        repo = git.Repo(local_path)
        #repo.submodule_update(init=True, recursive=True)
        repo.git.submodule('update', '--init', '--recursive', '--remote',
                           '--merge')


def get_folder_name(url):
    components = url.split('/')
    size = len(components)
    return components[size - 1]


def main():
    repositories = get_repo_list('./src/repositories.json')
    clone_repositories(repositories)


if __name__ == '__main__':
    main()
