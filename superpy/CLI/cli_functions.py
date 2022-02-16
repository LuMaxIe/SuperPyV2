import datetime
import csv
import json
from random import randint
import re
import plotext as plt

from plotext._utility import color, data, plot
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, FloatPrompt, IntPrompt, Prompt

from . import cli_theme

# Starting point of the application. If you want to add more functionalities, you must update the menu and
# the if/else statements in main
def cli_menu(used_menu, date_to_display):

    console = Console(theme=cli_theme.SuperPy_Theme)
    if not used_menu:
        console.print(Panel.fit("""Hi and welcome to SuperPy THE most powerful grocery assistant in the entire digital world!""", 
        title=str(date_to_display), style="info"))
        
    menu_choice = Prompt.ask('\nWhat would you like to do?: \n\n', choices=["review inventory", "review financials", "add products", 
    "add sales", "adjust date", "export inventory data", "exit superpy"])
        
    return menu_choice

# From here on each of the cli inventory will act as a mini menu / questionaire to get input from the user
# the application will then use the Inventory class (database) methods to perform the tasks.

# Creates and logs a Rich table in the terminal which can be sorted on a specified key.
def cli_inventory(database):
    console = Console(theme=cli_theme.SuperPy_Theme)
    want_sorting = Confirm.ask("\nDo you want to sort the overview on a certain key?", default="n")

    if want_sorting:
        key_sort = Prompt.ask("\nOn what key would you like the sorting to be done?", choices=["Id", "Product_Name", "Product_Group",
                      "Count", "Price", "Markup", "Sell_Price", "Expiration_Date", "Date_Product_Added"])
        want_reversed = Confirm.ask("\nDo you want to sort on a descending order? ('n' will order in ascending manner)")        
        # execute class method with the given parameters
        console.print(database.get_inventory_overview(key_sort, want_reversed))

    else:
        console.print(database.get_inventory_overview())

# function to add products manually or with a csv file into the database
def cli_add_products(database):
    addition_type = Prompt.ask("\nDo you want to add products manually or by uploading a file?\n\n", choices=["manually", "upload file", "go back", "exit superpy"])
    console = Console(theme=cli_theme.SuperPy_Theme)
    if addition_type == "manually":
        prod_list = []
        while True:
            prod_to_add = {
                "Product_Name": Prompt.ask("\nWhat is the name of the product?").lower().capitalize(),
                "Product_Group": Prompt.ask("\nTo what product group does it belong? (Fruit, meat, etc)", default="None").lower().capitalize(),
                "Count": IntPrompt.ask("\nHow many of pieces the product have you bought?", default=0),
                "Initial_Count": 0,
                "Price": FloatPrompt.ask("\nHow much did you pay for the product? (Per piece)", default=0.00),
                "Markup": FloatPrompt.ask("\nHow much markup would you like on this product? (In decimals: if you want 25% markup enter 1.25)", default=0.00),
                "Expiration_Date": database.date_obj + datetime.timedelta(IntPrompt.ask("\nPlease add in how many days the product will expire")),
                "Date_Product_Added": database.date_obj.strftime("%Y-%m-%d")
            }
            console.print(f"\nYou've entered the following product:\nName: {prod_to_add['Product_Name']}\nGroup: {prod_to_add['Product_Group']}\nAmount: {prod_to_add['Count']}\nPrice: {prod_to_add['Price']}\nMarkup: {prod_to_add['Markup']}\nExpiration date: {prod_to_add['Expiration_Date']}", style="info")
            input_is_correct = Confirm.ask("\nAdd product to product upload list?")
            if input_is_correct:
                prod_to_add["Initial_Count"] = prod_to_add["Count"]
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

# function to add sales to the database manually or by uploading a csv file
def cli_add_sales(database):
    addition_type = Prompt.ask("\nDo you want to add sales manually or by uploading a file?\n\n", choices=["manually", "upload file", "go back", "exit superpy"])
    console = Console(theme=cli_theme.SuperPy_Theme)
    if addition_type == "manually":
        sale_list = []
        while True:
            sale_to_add = {
                "name": Prompt.ask("\nWhat is the name of the product?").lower().capitalize(),
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
                            console.print("\nSuccesfully added the sale(s)!\n", style="info")
                        else:
                            raise ValueError
                    except ValueError:
                        console.print("\nAddition of sale(s) unsuccessful\n", style="info")

                    return
            else:
                continue

    elif addition_type == "upload file":
        has_file = Confirm.ask("\nDo you have a file ready to import in the 'Uploads/Ready_For_Import' folder?\n")
        if has_file:
            file_name = Prompt.ask("\nWhat is the file name?\n", default="Sales_Upload_Form.csv")
        if has_file:
            if file_name.endswith("csv"):
                with open(f"./Uploads/Ready_For_Import/{file_name}") as f:
                    reader = csv.DictReader(f)
                    database.sell_products(list(reader))
                    console.print("\nSuccesfully added the sales(s)!\n", style="info")
            else:
                console.print("File doesn't have the right extension (csv)\n", style="info")
        else:
            console.print("Please make your file ready for import and add it to the 'Ready_For_Import' folder\n", style="info")

    elif addition_type == "go back":
        return
    else:
        exit()

# function to fetch all financial data and show this in a graph
def cli_reports(database):
    report_days_back = IntPrompt.ask("\nHow many days back do you want to report on?\n\n", default=100)
    report_on_kpi_revenue = Confirm.ask("\nDo you want to add total revenue in your report?\n", default="y")
    report_on_kpi_costs = Confirm.ask("\nDo you want to add total costs in your report?\n", default="y")
    report_on_kpi_profit = Confirm.ask("\nDo you want to add total profit in your report?\n", default="y")
    base = database.date_obj
    date_list = [str(base - datetime.timedelta(days=x)) for x in range(report_days_back)]
    date_list.reverse()

    plt.datetime.set_datetime_form("%Y-%m-%d")

    revenue = []
    costs = []
    profit = []

    # Check for costs, profit and revenue data in database for each date point in the date list
    for date in date_list:

        found_sales_data = False
        found_bought_data = False

        # check if there was a sale on the date and add to list
        with open("./Database/Sales.json", 'r') as salesfile:
            sales_data = json.load(salesfile)

            for product in sales_data:
                product_sale_records = sales_data[product]
                for sale_entry in product_sale_records:
                    info = product_sale_records[sale_entry]
                    if info["Sell_Date"] == date:
                        found_sales_data = True
                        if len(revenue) == 0:
                            revenue.append(info["Total_Revenue"])
                            profit.append(info["Total_Profit"])
                        elif (len(revenue) - 1) == (date_list.index(date)) and len(revenue) != 0:
                            revenue[date_list.index(date)] = round(info["Total_Revenue"] + revenue[date_list.index(date)], 2)
                            profit[date_list.index(date)] = round(info["Total_Profit"] + profit[date_list.index(date)], 2)
                        else:
                            revenue.append(round(info["Total_Revenue"] + revenue[date_list.index(date) - 1], 2))
                            profit.append(round(info["Total_Profit"] + profit[date_list.index(date) - 1], 2))   

        # check if there was a buying action on the date in the list
        with open(database.data_path, 'r', newline='') as csvfile:
          invent_reader = csv.DictReader(csvfile, delimiter=',')
          for row in invent_reader:
              if row['Date_Product_Added'] == date:
                found_bought_data = True
                if len(costs) == 0:
                    costs.append(round(float(row["Price"]) * float(row["Initial_Count"]), 2))
                elif (len(costs) - 1) == date_list.index(date) and len(costs) != 0:
                    costs[date_list.index(date)] = costs[date_list.index(date) - 1] + round(float(row["Price"]) * float(row["Initial_Count"]), 2)
                else:
                    costs.append(round(float(row["Price"]) * float(row["Initial_Count"]), 2) + costs[date_list.index(date) - 1])

        # Extend the data in the lists with the previous value or 0
        if not found_sales_data:
            if len(revenue) == 0:
                revenue.append(0)
                profit.append(0)
            else:
                revenue.append(revenue[date_list.index(date) - 1])
                profit.append(profit[date_list.index(date) - 1])
        
        if not found_bought_data:
            if len(costs) == 0:
                costs.append(0)
            else:
                costs.append(costs[date_list.index(date) - 1])

    # Show report based on the asked input
    if report_on_kpi_profit:
        plt.plot_date(date_list, profit, label="Total Profit")
    if report_on_kpi_revenue:
        plt.plot_date(date_list, revenue, label="Total Revenue")
    if report_on_kpi_costs:
        plt.plot_date(date_list, costs, label="Total Costs")

    plt.canvas_color('grey')
    plt.axes_color('white')
    plt.title("Financial Report")
    plt.plot_size(width=100, height=30)
    plt.show()
    plt.clear_data()
    plt.clear_plot()
    
    return

def cli_export_data(database):
    console = Console(theme=cli_theme.SuperPy_Theme)

    selection_of_columns = list(database.invent_headers)
    selected_columns = []
    if not Confirm.ask(f"\nDo you want to include all columns in your export?\nColumns: {selection_of_columns}"):
        console.print(f"\nPlease make a selection out of {selection_of_columns}")
        for column in selection_of_columns:
            if Confirm.ask(f"\nDo you want to add: {column} into your report?"):
                selected_columns.append(column)

    console.print(f"\nSelected columns (empty list means all columns): {selected_columns}")

    want_sorting = Confirm.ask("\nDo you want to sort the export on a certain column?", default=False)

    file_name = Prompt.ask("Give a name/number for the file you want to download", default=randint(0, 100000))

    if want_sorting and len(selected_columns) == 0:
        key_sort = Prompt.ask("\nOn what column would you like the sorting to be done?", choices=selection_of_columns)
        want_reversed = Confirm.ask("\nDo you want to sort on a descending order? ('n' will order in ascending manner)")        
    elif want_sorting:
        key_sort = Prompt.ask("\nOn what column would you like the sorting to be done?", choices=selected_columns)
        want_reversed = Confirm.ask("\nDo you want to sort on a descending order? ('n' will order in ascending manner)")

    with open(database.data_path, 'r', newline='') as csvfile:
        invent_reader = csv.DictReader(csvfile, delimiter=',')
        with open(f"./Downloads/export_{database.date}_{file_name}.csv", "w+") as f:
            report_writer = csv.DictWriter(f, fieldnames= selection_of_columns if len(selected_columns) == 0 else selected_columns, lineterminator="\n")
            report_writer.writeheader()
            # Check if sorting of the table is needed.
            if want_sorting != False: 
                sort_table = sorted(list(invent_reader), key=lambda d: d[key_sort], reverse=want_reversed) if key_sort not in ["Count", 
                "Markup", "Sell_Price", "Id"] else sorted(list(invent_reader), key=lambda d: float(d[key_sort]), reverse=want_reversed)

                for row in sort_table:
                    adjusted_row = row.copy()
                    keys_to_include = selection_of_columns if len(selected_columns) == 0 else selected_columns
                    for row_item in row:
                        if row_item not in keys_to_include:
                            del adjusted_row[row_item]
                    report_writer.writerow(adjusted_row)
            # Write unsorted
            else:
                for row in invent_reader:
                    adjusted_row = row.copy()
                    keys_to_include = selection_of_columns if len(selected_columns) == 0 else selected_columns
                    for row_item in row:
                        if row_item not in keys_to_include:
                            del adjusted_row[row_item]
                    report_writer.writerow(adjusted_row)

    return
