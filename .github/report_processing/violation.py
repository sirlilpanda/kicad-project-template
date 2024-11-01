class Violation:
    def __init__(self, violation : dict, violation_report_type : str = ["erc", "drc"]) -> None:
        self.violation_type : str = \
         "warn" if violation["severity"] == "warning" else "error"
        self.name : str = violation["description"]
        self.content : str = ""

        # this violation_report_type purely exists because of a bug
        # in kicads json output format where json output on erc reports
        # the position in decimeters
        for item in violation["items"]:
            item_string = item["description"]
            x : float = float(item["pos"]["x"]) * (100.0 if (violation_report_type == "erc") else 1.0)
            y : float = float(item["pos"]["y"]) * (100.0 if (violation_report_type == "erc") else 1.0)
            # print(f"{x=}")
            
            item_string += f" at [x = {x:.4}mm, y = {y:.4}mm]\n"
            self.content += item_string 
