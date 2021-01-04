workspaceFolder :=

# https://gist.github.com/sighingnow/deee806603ec9274fd47
ifneq ($(OS),Windows_NT)
	workspaceFolder = ./
endif

pythonrequirements:
	pip install -r requirements.txt

get-repositories:
	python ${workspaceFolder}src/get-repositories.py

create-problems-list:
	python ${workspaceFolder}src/create-problems-list.py

update-repositories-md:
	python ${workspaceFolder}src/update-repositories-md.py

run-all-scripts:
	python ${workspaceFolder}src/run-scripts.py

all: pythonrequirements get-repositories create-problems-list update-repositories-md
