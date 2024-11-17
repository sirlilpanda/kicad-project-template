from violation import Violation
import datetime
import json
from pprint import pprint



def process_violation_list(drc_json : dict, list_name : str) -> None:
    if list_name in drc_json.keys():
        unconnected_items_errors = []
        unconnected_items_warns = []
        number_of_errors = 0
        number_of_warns = 0
        for violation in drc_json[list_name]:
            v = Violation(violation, "drc")
            if (v.violation_type == "error"):
                unconnected_items_errors.append(v)
                number_of_errors += 1
            if (v.violation_type == "warn"):
                unconnected_items_warns.append(v)
                number_of_warns += 1

        drc_json[list_name] = {
            "errors" : unconnected_items_errors,
            "warns" : unconnected_items_warns,
            "number_of_errors" : number_of_errors,
            "number_of_warns" : number_of_warns,
        }
    else:
        drc_json.setdefault(list_name, {})
        drc_json[list_name].setdefault("number_of_errors", 0)
        drc_json[list_name].setdefault("number_of_warns", 0)

def process_report(report : str) -> dict:
    out_dict : dict = json.loads(report)
    number_of_errors = 0;
    number_of_errors = 0;

    process_violation_list(out_dict, "unconnected_items")
    process_violation_list(out_dict, "violations")
    process_violation_list(out_dict, "schematic_parity")

    out_dict.setdefault(
        "total_errors", 
        out_dict["unconnected_items"]["number_of_errors"] +
        out_dict["violations"]["number_of_errors"] +
        out_dict["schematic_parity"]["number_of_errors"]
    )
    
    out_dict.setdefault(
        "total_warns", 
        out_dict["unconnected_items"]["number_of_warns"] +
        out_dict["violations"]["number_of_warns"] +
        out_dict["schematic_parity"]["number_of_warns"]
    )
    
    return out_dict