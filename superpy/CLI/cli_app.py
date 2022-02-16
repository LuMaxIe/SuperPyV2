import datetime
import json
from rich.console import Console
from rich.prompt import Prompt, Confirm

import time
import os.path

from Classes.product_inventory import Inventory

from . import cli_theme
from . import cli_functions

def cli_logic():
    # Theme and loading visual
    console = Console(theme=cli_theme.SuperPy_Theme)
    with console.status("Loading SuperPY", spinner="material"):
        time.sleep(2)
    console.print("\n")
    console.rule("[bold green]SuperPy")

    # Paths needed to use the program, these will be used with the setup part below
    db_path = "./Database"
    db_uploads = "./Uploads"
    db_uploads_template_folder = "./Uploads/Template"
    db_uploads_ready = "./Uploads/Ready_For_import"
    db_uploads_template = "./Uploads/Template/Upload_Form.csv"
    db_uploads_sales_template = "./Uploads/Template/Sales_Upload_Form.csv"
    db_inventory = "./Database/Inventory.csv"
    db_sales = "./Database/Sales.json"
    db_reports = "./Database/Reports.csv"


    # Application Set-up / Check for missing files
    while True:

        for item in [db_path, db_uploads, db_uploads_template_folder, db_uploads_ready, db_uploads_template, 
        db_uploads_sales_template, db_inventory, db_sales, db_reports]:
            if not os.path.exists(item):
                create_permission = Confirm.ask(f"""\n\nYou're missing the following folder/file: {item}, which is essential
                 for this program, do you want to create it?""")
                if not create_permission:
                    console.print("""SuperPY doesn't work without this file, please give permission or exit the program (Ctrl-c)""")
                else:
                    open(item, 'x') if "csv" in item or "json" in item else os.mkdir(item)
                    if item == "./Database/Sales.json":
                        with open(item, 'w+') as j:
                            json.dump({}, j)

        all_paths_exist = True
        for item in [db_path, db_uploads, db_uploads_template_folder, db_uploads_ready, 
        db_uploads_template, db_uploads_sales_template, db_inventory, db_sales, db_reports]:
            if not os.path.exists(item):
                all_paths_exist = False
        if all_paths_exist:
            break
    
    # Menu
    console.print("\n")
    menu_is_used = False
    date_adjustment = 0
    while True: 
        db = Inventory("./Database/Inventory.csv", "./Database/Sales.json", "./Uploads/Template/Upload_Form.csv", 
        "./Uploads/Template/Sales_Upload_Form.csv", date_adjustment)
        menu_choice = cli_functions.cli_menu(menu_is_used, db.date)

        if menu_choice == "review inventory":
            cli_functions.cli_inventory(db)
            menu_is_used = True
            continue
        elif menu_choice == "generate reports":
            cli_functions.cli_reports(db)
            menu_is_used = True
            continue
        elif menu_choice == "add products":
            cli_functions.cli_add_products(db)
            menu_is_used = True
            continue
        elif menu_choice == "adjust date":
            date_adjustment = int(Prompt.ask(f"\nWith how many days would like to adjust the current date? {datetime.date.today()}"))
            menu_is_used = True
            continue
        elif menu_choice == "add sales":
            cli_functions.cli_add_sales(db)
            menu_is_used = True
            continue
        elif menu_choice == "export inventory data":
            cli_functions.cli_export_data(db)
            menu_is_used = True
            continue
        elif menu_choice == "exit superPY":
            break
        return