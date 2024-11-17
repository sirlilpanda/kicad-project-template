# usage: python process_json_reports.py report.json template.mustache outfile.md project_name
import chevron 
import sys
import datetime
import json
import process_erc_json
import process_drc_json
from pprint import pprint


def load_report(filename : str, project_name : str) -> dict:
    out_dict : dict = {}
    with open(filename, "r") as js:
        if ("erc" in filename.lower()):
            out_dict = process_erc_json.process_report(js.read())
        if ("drc" in filename.lower()):
            out_dict = process_drc_json.process_report(js.read())

    out_dict.setdefault(
        "time", 
        str(datetime.datetime.now().time())
    )
    
    out_dict.setdefault(
        "date", 
        str(datetime.datetime.now().date().strftime("%d-%m-%Y"))
    )

    out_dict.setdefault(
        "project_name",
        project_name
    )
    
    out_dict.setdefault(
        "has_violations",
        True if out_dict["total_warns"] + out_dict["total_errors"] else None
    )

    return out_dict

def main():
    report_hash = load_report(sys.argv[1], sys.argv[4])
    # pprint(report_hash)
    with open(sys.argv[2], "r") as txt:
        out = chevron.render(txt.read(), report_hash)
        with open(sys.argv[3], "w") as md:
            md.write(out)

if __name__ == "__main__":
    main()