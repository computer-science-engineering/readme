import os
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
    shutil.rmtree(dir, onerror=remove_readonly)


# git config --system core.longpaths true
def clone_repositories(list):
    parent_folder = './repositories'
    clean_repositories_dir(parent_folder)
    if not os.path.exists(parent_folder):
        os.makedirs(parent_folder)
    for item in list:
        folder_name = get_folder_name(item['url'])
        git.Repo.clone_from(item['url'],
                            os.path.join(parent_folder, folder_name))


def get_folder_name(url):
    components = url.split('/')
    size = len(components)
    return components[size - 1]


def main():
    repositories = get_repo_list('./src/repositories.json')
    clone_repositories(repositories)


if __name__ == '__main__':
    main()
