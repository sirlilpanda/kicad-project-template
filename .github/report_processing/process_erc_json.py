from violation import Violation
import datetime
import json

class Sheet:
    def __init__(self, json_obj : dict) -> None:
        self.name : str = json_obj["path"]
        self.number_of_errors : int = 0
        self.number_of_warns : int = 0
        self.errors : list[Violation] = list()
        self.warns : list[Violation] = list()

        for violation in json_obj["violations"]:
            v = Violation(violation, "erc")
            if (v.violation_type == "error"):
                self.errors.append(v)
                self.number_of_errors += 1
            if (v.violation_type == "warn"):
                self.warns.append(v)
                self.number_of_warns += 1

    def to_dict(self) -> dict:
        out_dict = self.__dict__
        errors_strings = []
        warns_strings = []

        for error in out_dict["errors"]:
            errors_strings.append(error.__dict__)
        out_dict["errors"] = errors_strings
        
        for warn in out_dict["warns"]:
            warns_strings.append(warn.__dict__)
        out_dict["warns"] = warns_strings
        
        return out_dict

def process_report(report : str) -> dict:
    out_dict : dict = json.loads(report)

    sheets = [Sheet(sheet) for sheet in out_dict["sheets"]]
    out_dict["sheets"] = [sheet.to_dict() for sheet in sheets]

    out_dict.setdefault(
        "total_errors", 
        sum(sheet.number_of_errors for sheet in sheets)    
    )
    out_dict.setdefault(
        "total_warns", 
        sum(sheet.number_of_warns for sheet in sheets)    
    )

    return out_dict