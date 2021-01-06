workspaceFolder :=

# https://gist.github.com/sighingnow/deee806603ec9274fd47
ifneq ($(OS),Windows_NT)
	workspaceFolder = ./
endif

pythonrequirements:
	pip install -r requirements.txt

get-repositories:
	python ${workspaceFolder}src/get_repositories.py

create-problems-list:
	python ${workspaceFolder}src/create_problems_list.py

update-repositories-md:
	python ${workspaceFolder}src/update_repositories_md.py

run-all-scripts:
	python ${workspaceFolder}src/run_scripts.py

all: pythonrequirements get-repositories create-problems-list update-repositories-md
