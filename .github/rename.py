from pathlib import Path
import os
import sys
from ruamel.yaml import YAML

def rename_project(project_name, new_name = "template"):
    """renames the kicad project"""
    project_path = str(Path(f"Hardware/{project_name}_PROJECT"))
    files = os.listdir(project_path)

    for index, file in enumerate(files):
        print(file)
        os.rename(os.path.join(project_path, file), os.path.join(project_path, file.replace(project_name, new_name)))

    os.rename(project_path, project_path.replace(project_name, new_name))

    pcb_path = str(Path(f"Hardware/{project_name}_PCB"))
    os.rename(pcb_path, pcb_path.replace(project_name, new_name))

    doc_path = str(Path(f"Hardware/{project_name}_DOCS"))
    os.rename(doc_path, doc_path.replace(project_name, new_name))

def main():
    yaml : YAML = YAML() 
    with open(Path("project_settings.yaml"), "r") as yaml_file:
        settings = yaml.load(yaml_file)
        
    print(f"{settings['project_name']=}")
    print(f"{settings=}")
    rename_project(settings["project_name"], sys.argv[1])
    settings["project_name"] = sys.argv[1]
    settings["has_been_set_up"] = True
    # have to just print it out a rewrite over .project_settings because this guy
    # is dumb and doesnt just let you write these out to string
    with open(Path("project_settings.yaml"), "w", encoding=("utf-8")) as file:
        yaml.dump(settings, file)     


if __name__ == "__main__":
    main()