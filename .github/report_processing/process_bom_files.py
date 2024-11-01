# look it would be piss easy to just keep it as a CSV but we can post process to add cool things like cost to each of the parts
import csv
import sys
import chevron 
import datetime
from pprint import pprint

file_path_delimter = "\\" if sys.platform == "win32" else "/"

def load_bom(filename : str) -> dict:
    out_dict = {
        "parts" : [],
        "time" : str(datetime.datetime.now().time()),
        "date" : str(datetime.datetime.now().date().strftime("%d-%m-%Y")),
        "total_cost" : 0,
        "total_parts" : 0,
        "project_name" : filename.strip(".csv").strip("bom").split(file_path_delimter)[-1]
    }
    
    with open(filename, "r") as csv_file:
        for row in csv.DictReader(csv_file):
            part_cost = 0
            out_dict["total_parts"] += 1
            out_dict["parts"].append(
                {
                    "Reference" : row["Refs"], 
                    "Value" : row["Value"], 
                    "Quantity" : row["Qty"], 
                    "part_number" : row["Footprint"], 
                    "cost" : part_cost, # add some API call somewhere here
                }
            )
    return out_dict

def main():
    report_hash = load_bom(sys.argv[1])
    # pprint(report_hash)
    with open(sys.argv[2], "r") as txt:
        out = chevron.render(txt.read(), report_hash)
        with open(sys.argv[3], "w") as md:
            md.write(out)



if __name__ == "__main__":
    main()