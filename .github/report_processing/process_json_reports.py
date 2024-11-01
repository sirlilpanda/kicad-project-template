# usage: python process_json_reports.py report.json template.mustache outfile.md
import chevron 
import sys
import datetime
import json
import process_erc_json
import process_drc_json
from pprint import pprint


def load_report(filename : str) -> dict:
    out_dict : dict = {}
    with open(filename, "r") as js:
        if ("erc" in filename.lower()):
            out_dict = process_erc_json.process_report(js.read())
        if ("drc" in filename.lower()):
            out_dict = process_drc_json.process_report(js.read())

    out_dict.setdefault("time", str(datetime.datetime.now().time()))
    out_dict.setdefault("date", str(datetime.datetime.now().date().strftime("%d-%m-%Y")))

    return out_dict

def main():
    report_hash = load_report(sys.argv[1])
    # pprint(report_hash)
    with open(sys.argv[2], "r") as txt:
        out = chevron.render(txt.read(), report_hash)
        with open(sys.argv[3], "w") as md:
            md.write(out)

if __name__ == "__main__":
    main()