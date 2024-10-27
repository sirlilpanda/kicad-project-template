## yes im using these for a cross platform way to run commands
import sys
import os
import subprocess
from pathlib import Path

kicad_cli_path = "kicad-cli"
project_name = "template"

if (sys.platform == "darwin"):
    kicad_cli_path = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"

help_message = """
this is a python script that is a thin wrapper around kicad-cli as well as some configurating commands for the project

usage: python tools.py {command} {command_args}

commands:

    rename: this renames the kicad project
        python tools.py rename {project_name}

    change_path: changes the path of where kicad-cli is
        python tools.py change_path {new_path} 
    
    pdf: creates a pdf of the kicad schmatic
        python tools.py pdf {output = Hardware_Docs}
    
    pcb: creates the PDB of the project
        python tools.py pcb {output = Hardware_{project_name}_PCB/}

    bom: creates the BOM of the project
        python tools.py bom {output = Hardware_Docs/BOM/}
        
"""

def check_kiCad_exists(kicad_cli_name : str = "kicad-cli") -> bool:
    try:
        subprocess.run(f"{kicad_cli_name}", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True;
    except Exception as err:
        print("[ERROR] kicad-cli command does not exists")
        if (kicad_cli_name != "kicad-cli"):
            print(f"you entered {kicad_cli_name} for an alias for the kicad-cli command, check if this is correct")
        print("you got error : \n" + "="*20)
        print(err)
        print("\n"+ "="*20)
        return False;

def change_var_declaration(var_name, new_declaration):
    file = ""
    with open(__file__, "r") as txt:
        file = txt.read()

    varible_declaration = f"{var_name} = "

    kicad_cli_path_index = file.find(varible_declaration) + len(varible_declaration)
    kicad_cli_path_end_index = file.find("\n", kicad_cli_path_index)

    old_path = file[kicad_cli_path_index:kicad_cli_path_end_index]
    
    with open(__file__, "w") as txt:
        txt.write(file.replace(old_path, f'"{new_declaration}"'))

def rename_project(new_name = "template"):
    """renames the kicad project"""

    path = str(Path(f"Hardware/{project_name}"))
    files = os.listdir(path)

    for index, file in enumerate(files):
        print(file)
        os.rename(os.path.join(path, file), os.path.join(path, file.replace(project_name, new_name)))

    os.rename(path, path.replace(project_name, new_name))
    os.rename(path, path.replace(project_name+"_PCB", new_name+"_PCB"))

    change_var_declaration(project_name, new_name)

def set_kicad_cli_path(new_path = "kicad-cli"):
    change_var_declaration(kicad_cli_path, new_path)

def create_pdf(output = "_defualt_"):
    if not check_kiCad_exists(): return
        
    main_sch_path = Path(os.curdir) / Path("Hardware") / Path(project_name) / Path(project_name + ".kicad_sch")
    output_path = Path(os.curdir) / Path("Hardware_Docs") / Path(output + ".pdf")

    if output == "_defualt_":
        output_path = Path(os.curdir) / Path("Hardware_Docs") / Path(project_name + ".pdf")

    exit_code, string = subprocess.getstatusoutput(f"{kicad_cli_path} sch export pdf -o {output_path} {main_sch_path}")

    if exit_code > 0:
        print("[ERROR] could not create pdf got error:\n" + "="*20)
        print(string)
        print("\n"+ "="*20)

def create_PCB(output_path_name = "_defualt_"):
    if not check_kiCad_exists(): return
        
    pcb_path = Path(os.curdir) / Path("Hardware") / Path(project_name) / Path(project_name + ".kicad_pcb")
    output_path = Path(os.curdir) / Path("Hardware") / Path(output_path_name)

    if output_path_name == "_defualt_":
        output_path = Path(os.curdir) / Path("Hardware") / Path(project_name+"_PCB")

    print(output_path)

    exit_code, string = subprocess.getstatusoutput(f"{kicad_cli_path} pcb export gerbers -o {output_path} {pcb_path}")

    if exit_code > 0:
        print("[ERROR] could not create pdf got error:\n" + "="*20)
        print(string)
        print("\n"+ "="*20)

    exit_code, string = subprocess.getstatusoutput(f"{kicad_cli_path} pcb export drill -o {output_path} {pcb_path}")

    if exit_code > 0:
        print("[ERROR] could not create pdf got error:\n" + "="*20)
        print(string)
        print("\n"+ "="*20)

def create_BOM(output = "_defualt_"):
    if not check_kiCad_exists(): return
    main_sch_path = Path(os.curdir) / Path("Hardware") / Path(project_name) / Path(project_name + ".kicad_sch")
    output_path = Path(os.curdir) / Path("Hardware_Docs") / Path("BOM") / Path(output + ".csv")

    if output == "_defualt_":
        output_path = Path(os.curdir) / Path("Hardware_Docs") / Path("BOM") / Path(project_name + ".csv")

    exit_code, string = subprocess.getstatusoutput(f"{kicad_cli_path} sch export bom -o {output_path} {main_sch_path}")

    if exit_code > 0:
        print("[ERROR] could not create pdf got error:\n" + "="*20)
        print(string)
        print("\n"+ "="*20)


if __name__ == "__main__":
    match sys.argv[1:]:
        case ("pdf", name):
            create_pdf(name)
        case ("pdf",):
            create_pdf() 

        case ("pcb", output_path):
            create_PCB(output_path)
        case ("pcb",):
            create_PCB()

        case ("bom", output_path):
            create_BOM(output_path)
        case ("bom",):
            create_BOM()

        case ("rename", new_name):
            rename_project(new_name, project_name)    
        case ("change_path", new_path):
            set_kicad_cli_path(new_path)

        case (unknown_command):
            if (len(unknown_command)):
                print("unknown command got : " + " ".join(unknown_command))
            else:
                print("got not command line args")
            print(help_message)

    # print(check_kiCad_exists("k"));


