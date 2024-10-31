# usage: python process_rpt_files.py report.rpt template.mustache outfile.md
# so this was useless
import chevron 
import sys
import datetime

class Error:
    def __init__(self) -> None:
        self.name : str
        self.content : str
        self.loction : str

    @classmethod
    def from_lines(self, lines : list[str]) -> "Warn":
        error = Error()
        error.name = lines[0].split(":", 1)[1].strip()
        error.content = lines[2].split(":", 1)[1].strip()
        error.loction = lines[2].split(":", 1)[0].strip()
        return error

class Warn:
    def __init__(self) -> None:
        self.name : str
        self.content : str
        self.loction : str

    @classmethod
    def from_lines(self, lines : list[str]) -> "Warn":
        warn = Warn()
        warn.name = lines[0].split(":", 1)[1].strip()
        warn.content = lines[2].split(":", 1)[1].strip()
        warn.loction = lines[2].split(":", 1)[0].strip()
        return warn

class Sheet:
    def __init__(self) -> None:
        self.name : str = ""
        self.number_of_errors : int = 0
        self.number_of_warns : int = 0
        self.errors : list[Error] = list()
        self.warns : list[Warn] = list()

    @classmethod
    def from_string(self, string : str) -> "Sheet":
        sheet = Sheet()
        lines = string.splitlines()
        sheet.name = lines[0].replace("Sheet", "", 1).strip()
        lines = lines[1:]
        for i in range(0, len(lines[1:]), 3):
            if ("warning" in lines[i+1]):
                sheet.warns.append(Warn.from_lines(lines[i:i+3]))
                sheet.number_of_warns += 1
            if ("error" in lines[i+1]):
                sheet.errors.append(Error.from_lines(lines[i:i+3]))
                sheet.number_of_errors += 1

        return sheet

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

class ReportHash:
    def __init__(self, report_type, time_created, total_errors, total_warns, sheets) -> None:
        self.report_creation_time : datetime = time_created
        
        self.report_type = \
            "ERC" if (report_type == "erc") else "DRC"
        self.report_type_name = \
            "eletronic" if (report_type == "erc") else "design"
        
        self.total_warns : int = total_warns
        self.total_errors : int = total_errors
        self.sheets : list[Sheet] = sheets

    def to_dict(self) -> dict:
        out_dict = self.__dict__

        out_dict.setdefault("time", self.report_creation_time.time())
        out_dict.setdefault("date", self.report_creation_time.date())
        sheets : list[dict] = []
        for sheet in out_dict["sheets"]:
            sheets.append(sheet.to_dict())
        out_dict["sheets"] = sheets
        return out_dict

def load_report(filename : str) -> ReportHash:
    time_created : datetime = None
    report_string : str = ""
    with open(filename, "r") as rpt:
        # header = rpt.readline().strip()
        # time_format_string = header[12:].split(",")[0]
        time_created = datetime.datetime.now()
        report_string = rpt.read()

    report_string_lines = report_string.splitlines() 
    end_string : str = report_string_lines[-1].split(" ")
    report_type = end_string[2].lower()
    total_errors = int(end_string[7])
    total_warns  = int(end_string[10])
    sheets_list = "\n".join(report_string_lines[:-1]).split("*****")[1:]
    
    return ReportHash(
        report_type, 
        time_created, 
        total_errors, 
        total_warns,
        [Sheet.from_string(sheet_string) for sheet_string in sheets_list]
    )

def main():
    report_hash = load_report(sys.argv[1])
    with open(sys.argv[2], "r") as txt:
        out = chevron.render(txt.read(), report_hash.to_dict())
        with open(sys.argv[3], "a") as md:
            md.write(out)
        
if __name__ == "__main__":
    main()


# hash:
# {
#     report_type : {ERC | DRC},
#     report_type : {eletronic | design},
#     total_warns : number,
#     total_errors: number,
#     sheets : [
#         {
#             name : sheet_name,
#             number_of_errors : number,
#             number_of_warns : number,
#             errors : [
#                 {
#                     error_name : string,
#                     error_content : string,
#                     error_loction : string,
#                 },
#                 ...
#             ],
#             warns : [
#                 {
#                     warn_name : string,
#                     warn_content : string,
#                     warn_loction : string,
#                 },
#                 ...
#             ]
#         },
#         ...
#     ]
# }
