import chevron 
import sys
import datetime
import json
import glob

from pprint import pprint



def load_json_file(filename : str) -> dict:
    with open(filename, "r") as js:
        return json.loads(js.read())

def create_hash(filenames : list[str]) -> dict:
    reports_dicts = []
    for report_name in filenames:
        reports_dicts.append(load_json_file(report_name))

    pprint(reports_dicts)


def main():
    print(sys.argv)

    readme_template, args = sys.argv[1:]



    report_hash = create_hash(args)

    with open(readme_template, "r") as txt:
        out = chevron.render(txt.read(), report_hash)
        # with open("README.md", "w") as md:
        #     md.write(out)

if __name__ == "__main__":
    main()