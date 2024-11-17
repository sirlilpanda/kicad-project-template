import chevron 
import sys
import datetime
import json
import glob
from pathlib import Path

from pprint import pprint


# erc
# {
#   "project_name" : "string",
#   "passing_erc" : "bool",
#   "erc_summary_link" : "link",  
# }

# drc
# {
#   "project_name" : "string",
#   "passing_drc" : "bool",
#   "drc_summary_link" : "link",  
# }

# project
# {
#     "project_name" : "string",
#     "project_link" : "link",
#     "schematic_link" : "link",
#     "gerber_link" : "link",
#     "bom_report_link" : "link",
#     "bom_csv_link" : "link"
# }

EXTRAS_FILENAME = "readme_extras.json"

def load_json_file(filename : str) -> dict:
    with open(Path(f"{filename}/{filename}"), "r") as js:
        return json.loads(js.read())

def create_hash(filenames : list[str]) -> dict:
    report_outs = filenames
    report_outs.remove("readme_extras.json")

    extras = {}
    with open("readme_extras.json", "r") as js:
        extras = json.loads(js.read())
    
    reports_dicts : list[dict] = []
    for report_name in report_outs:
        reports_dicts.append(load_json_file(report_name))

    readme_hash = {
        **extras,
        "projects" : [],
        "did_error" : False,
        "multiple_projects" : None
    }
    for report in reports_dicts:
        for project in readme_hash["projects"]:
            if project["project_name"] == report["project_name"]:
                for key in report.keys():
                    project.setdefault(key, report[key])
                break
        else:
            readme_hash["projects"].append(report)

    pprint(readme_hash)

    for project in readme_hash["projects"]:
        readme_hash["did_error"] |= not project["passing_erc"]
        readme_hash["did_error"] |= not project["passing_drc"]
        project.setdefault("passing_erc_emoji", "✅" if project["passing_erc"] == "true" else "❌") 
        project.setdefault("passing_drc_emoji", "✅" if project["passing_drc"] == "true" else "❌") 

    readme_hash["multiple_projects"] = True if len(readme_hash["projects"]) > 1 else None

    pprint(readme_hash)
    return readme_hash

def main():
    print(sys.argv)

    readme_template, *args = sys.argv[1:]

    report_hash = create_hash(args)

    with open(readme_template, "r") as txt:
        out = chevron.render(txt.read(), report_hash)
        with open("README.md", "w") as md:
            md.write(out)

if __name__ == "__main__":
    main()