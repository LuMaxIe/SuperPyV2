import datetime
import csv
import json

import plotext as plt
from plotext._utility import color, plot

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, FloatPrompt, IntPrompt, Prompt

from . import cli_theme

def cli_menu(used_menu, date_to_display):

    console = Console(theme=cli_theme.SuperPy_Theme)
    if not used_menu:
        console.print(Panel.fit("Hi and welcome to SuperPy THE most powerful grocery assistant in the entire digital world!", title=str(date_to_display), style="info"))
        
    menu_choice = Prompt.ask('\nWhat would you like to do?: \n\n', choices=["review inventory", "generate reports", "add products", "add sales", "adjust date", "exit superpy"])
        
    return menu_choice


def cli_inventory(database):
    console = Console(theme=cli_theme.SuperPy_Theme)
    want_sorting = Confirm.ask("\nDo you want to sort the overview on a certain key?")
    if want_sorting:
        key_sort = Prompt.ask("\nOn what key would you like the sorting to be done?", choices=["Id", "Product_Name", "Product_Group",
                      "Count", "Price", "Markup", "Sell_Price", "Expiration_Date", "Date_Product_Added"])
        want_reversed = Confirm.ask("\nDo you want to sort on a descending order? ('n' will order in ascending manner)")
        console.print(database.get_inventory_overview(key_sort, want_reversed))
    else:
        console.print(database.get_inventory_overview())


def cli_add_products(database):
    addition_type = Prompt.ask("\nDo you want to add products manually or by uploading a file?\n\n", choices=["manually", "upload file", "go back", "exit superpy"])
    console = Console(theme=cli_theme.SuperPy_Theme)
    if addition_type == "manually":
        prod_list = []
        while True:
            prod_to_add = {
                "Product_Name": Prompt.ask("\nWhat is the name of the product?").lower(),
                "Product_Group": Prompt.ask("\nTo what product group does it belong? (Fruit, meat, etc)", default="None").lower(),
                "Count": IntPrompt.ask("\nHow many of pieces the product have you bought?", default=0),
                "Price": FloatPrompt.ask("\nHow much did you pay for the product? (Per piece)", default=0.00),
                "Markup": FloatPrompt.ask("\nHow much markup would you like on this product? (In decimals: if you want 25% markup enter 1.25)", default=0.00),
                "Expiration_Date": datetime.date.today() + datetime.timedelta(IntPrompt.ask("\nPlease add in how many days the product will expire")),
                "Date_Product_Added": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            console.print(f"\nYou've entered the following product:\nName: {prod_to_add['Product_Name']}\nGroup: {prod_to_add['Product_Group']}\nAmount: {prod_to_add['Count']}\nPrice: {prod_to_add['Price']}\nMarkup: {prod_to_add['Markup']}\nExpiration date: {prod_to_add['Expiration_Date']}", style="info")
            input_is_correct = Confirm.ask("\nAdd product to product upload list?")
            if input_is_correct:
                prod_list.append(prod_to_add)
                add_another = Confirm.ask("\nDo you want to add another product?")
                if add_another:
                    continue
                else:
                    database.add_product(prod_list)
                    console.print("\nSuccesfully added the product(s)!", style="info")
                    return
            else:
                continue
    elif addition_type == "upload file":
        has_file = Confirm.ask("\nDo you have a file ready to import in the 'Uploads/Ready_For_Import' folder?")
        if has_file:
            file_name = Prompt.ask("\nWhat is the file name?", default="Upload_Form.csv")
        if has_file:
            if file_name.endswith("csv"):
                with open(f"./Uploads/Ready_For_Import/{file_name}") as f:
                    reader = csv.DictReader(f)
                    database.add_product(list(reader))
                    console.print("\nSuccesfully added the product(s)!", style="info")
            else:
                console.print("File doesn't have the right extension (csv)", style="info")
        else:
            console.print("Please make your file ready for import and add it to the 'Ready_For_Import' folder", style="info")

    elif addition_type == "go back":
        return
    else:
        exit()

def cli_add_sales(database):
    addition_type = Prompt.ask("\nDo you want to add sales manually or by uploading a file?\n\n", choices=["manually", "upload file", "go back", "exit superpy"])
    console = Console(theme=cli_theme.SuperPy_Theme)
    if addition_type == "manually":
        sale_list = []
        while True:
            sale_to_add = {
                "name": Prompt.ask("\nWhat is the name of the product?"),
                "amount": IntPrompt.ask("\nHow many of pieces the product have you sold?", default=0),
            }
            console.print(f"\nYou've entered the following sale:\nName: {sale_to_add['name']}\nAmount: {sale_to_add['amount']}", style="info")
            input_is_correct = Confirm.ask("\nAdd sale to sale upload list?")
            if input_is_correct:
                sale_list.append(sale_to_add)
                add_another = Confirm.ask("\nDo you want to add another sale?")
                if add_another:
                    continue
                else:
                    try:
                        if database.sell_products(sale_list) != 0:
                            console.print("\nSuccesfully added the sale(s)!", style="info")
                        else:
                            raise ValueError
                    except ValueError:
                        console.print("\nAddition of sale(s) unsuccessful\n", style="info")

                    return
            else:
                continue
    elif addition_type == "upload file":
        has_file = Confirm.ask("\nDo you have a file ready to import in the 'Uploads/Ready_For_Import' folder?")
        if has_file:
            file_name = Prompt.ask("\nWhat is the file name?", default="Sales_Upload_Form.csv")
        if has_file:
            if file_name.endswith("csv"):
                with open(f"./Uploads/Ready_For_Import/{file_name}") as f:
                    reader = csv.DictReader(f)
                    database.sell_products(list(reader))
                    console.print("\nSuccesfully added the sales(s)!", style="info")
            else:
                console.print("File doesn't have the right extension (csv)", style="info")
        else:
            console.print("Please make your file ready for import and add it to the 'Ready_For_Import' folder", style="info")

    elif addition_type == "go back":
        return
    else:
        exit()


def cli_reports(database):
    reporting_type = Prompt.ask("\nWhat do you want to report on?\n\n", choices=["sales", "csv export", "go back", "exit superpy"])
    console = Console(theme=cli_theme.SuperPy_Theme)
    
    plot_arr = []
    with open("./Database/Sales.json", 'r') as salesfile:
        sales_data = json.loads(salesfile)
        for product in sales_data:
            prod_sale_arr = []
            prod_sale_arr.append(product)
            sale_nums = []
            for sale in product:
                print(sale)
                sale_nums.append(sale.amount)
            prod_sale_arr.append(sale_nums)
            plot_arr.append(prod_sale_arr)

    print(plot_arr)    

    # x = [6, 7, 8, 9, 1, 4, 4, 5]
    # y = [1, 5, 3, 8, 4, 9, 0, 5]
    # plt.canvas_color('black')
    # plt.axes_color('white')
    # plt.title("Sales Report")
    # plt.plot_size(width=100, height=30)
    # plt.plot(y, color='white',)
    # plt.plot(x, color='red')
    # plt.show()



    # matplotlib
    # csv output
    return