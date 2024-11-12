import sys
import yaml
from pathlib import Path


def main():
    # "../project_settings.yaml"
    with open(Path(sys.argv[1])) as txt:
        project_settings = yaml.safe_load(txt.read())
        project_name = project_settings["project_name"]
        subnames = project_settings["sub_pcb_names"]
        print(f"matrix={[project_name] + subnames}")

if __name__ == "__main__":
    main()