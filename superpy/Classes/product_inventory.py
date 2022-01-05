import csv
import datetime
import random
import json
from rich.table import Table

class Inventory:
    # Standard headers used to create the inventory & sales file
    invent_headers = ["Id", "Product_Name", "Product_Group",
                      "Count", "Initial_Count", "Price", "Markup", "Sell_Price", 
                      "Expiration_Date", "Date_Product_Added"]
    sales_headers = ["name", "amount"]
    

    def __init__(self, inventory_database_path, sales_database_path, upload_path, sales_upload_path, date_adjust=0):
        self.date = str(datetime.date.today() + datetime.timedelta(date_adjust))
        self.date_obj = datetime.date.today() + datetime.timedelta(date_adjust)
        self.data_path = inventory_database_path
        self.sales_database_path = sales_database_path

        # Check if the inventory database file has (the correct) headers and, if not, create them
        with open(inventory_database_path, 'r+', newline='') as csvfile:
          invent_reader = csv.DictReader(csvfile)
          invent_writer = csv.DictWriter(csvfile, self.invent_headers ,lineterminator="\n")
          
          has_headers = invent_reader.fieldnames

          if has_headers == None:
            invent_writer.writeheader()
          else:
            for header in has_headers:
              if header not in self.invent_headers:
                invent_writer.writeheader()
        
        # Check and add headers to upload template
        with open(upload_path, 'r+', newline='') as csvfile:
          invent_reader = csv.DictReader(csvfile)
          invent_writer = csv.DictWriter(csvfile, self.invent_headers ,lineterminator="\n")
          
          has_headers = invent_reader.fieldnames

          if has_headers == None:
            invent_writer.writeheader()
          else:
            for header in has_headers:
              if header not in self.invent_headers:
                invent_writer.writeheader()
          
          # Add examples to product upload_form template
          if len(list(invent_reader)) == 0:
            invent_writer.writerow({
                "Id": "Auto generated leave field empty!",
                "Product_Name": "Apple",
                "Product_Group": "Fruit",
                "Count": 500,
                "Initial_Count": "Auto generated leave field empty!",
                "Price": 0.25,
                "Markup": 1.25,
                "Sell_Price": "Auto generated leave field empty!",
                "Expiration_Date": "2021-12-28",
                "Date_Product_Added": "Auto generated leave field empty!"
            })
        
        # Add headers to sales template
        with open(sales_upload_path, 'r+', newline='') as csvfile:
            invent_reader = csv.DictReader(csvfile)
            invent_writer = csv.DictWriter(csvfile, self.sales_headers ,lineterminator="\n")
            
            has_headers = invent_reader.fieldnames

            if has_headers == None:
              invent_writer.writeheader()
            else:
              for header in has_headers:
                if header not in self.sales_headers:
                  invent_writer.writeheader()
            
            # Add examples to sales upload template
            if len(list(invent_reader)) == 0:
              invent_writer.writerow({
                  "name": "Apple",
                  "amount": 30
              })

    # Function to return inventory data from a file as a table to display with "Rich"
    def get_inventory_overview(self, sort_key=None, is_reversed=False):

        table = Table(title=f"\nInventory overview: {self.date}")

        for header in self.invent_headers:
          table.add_column(header, no_wrap=False, style="green")

        with open(self.data_path, 'r', newline='') as csvfile:
          invent_reader = csv.DictReader(csvfile, delimiter=',')
          # Check if sorting of the table is needed.
          if sort_key != None: 
            sort_table = sorted(list(invent_reader), key=lambda d: d[sort_key], reverse=is_reversed) if sort_key not in ["Count", 
            "Markup", "Sell_Price", "Id"] else sorted(list(invent_reader), key=lambda d: float(d[sort_key]), reverse=is_reversed)
            for row in sort_table:
              table.add_row(row["Id"], row["Product_Name"], row["Product_Group"], 
                            row["Count"], row["Initial_Count"], row["Price"], row["Markup"], 
                            row["Sell_Price"], row["Expiration_Date"], row["Date_Product_Added"])
          else:
            for row in invent_reader:
              table.add_row(row["Id"], row["Product_Name"], row["Product_Group"], 
                            row["Count"], row["Initial_Count"], row["Price"], row["Markup"], 
                            row["Sell_Price"], row["Expiration_Date"], row["Date_Product_Added"])
        
        return table
    
    # Function to add products to the inventory file
    def add_product(self, products: list):

        with open(self.data_path, 'a+', newline='') as csvfile:
          invent_reader = csv.DictReader(csvfile, delimiter=',')
          for product in products:
            prod_to_add = product

            # Add unqiue Id for product
            id_list = []
            for row in invent_reader:
              id_list.append(row['Id'])
            while True:
              rando = round(random.randint(100000, 999999))
              if not rando in id_list:
                prod_to_add['Id'] = rando
                break
            
            # Calculate and add product selling price
            prod_to_add["Sell_Price"] = round((float(product["Price"]) * float(product["Markup"])), 2)
            prod_to_add["Date_Product_Added"] = self.date

            invent_writer = csv.DictWriter(csvfile, self.invent_headers, delimiter=',')
            invent_writer.writerow(prod_to_add)

    def sell_products(self, products: list):
          try:
            found_product = False
            for sold_product in products:
              product_name = sold_product["name"]
              amount = int(sold_product["amount"])
              sale_num = 0
              
              with open(self.sales_database_path, 'r') as jf:
              # Unique sales id check from json sales file
                data = json.load(jf)
                sale_id_list = []
                for prod in data:
                  for sale_id in prod:
                    if sale_id not in sale_id_list:
                      sale_id_list.append(sale_id)
                while True:
                  new_id = random.randint(10000, 99999)
                  if not new_id in sale_id_list:
                    sale_num = new_id
                    break

              # storage for lines to be rewritten
              adjusted_rows = []
              # counter to keep track of how many of the product there are left to sell
              sold_number = amount
              # create sale object
              sales_report_item = {
                product_name: {
                  sale_num: {
                    "Sell_Date": self.date,
                    "Total_Revenue": 0.00,
                    "Total_Cost": 0.00,
                    "Total_Profit": 0.00,
                    "Sold_Product_Ids": {}
                  }
                }
              }
            

              with open(self.data_path, 'r', newline='') as csvfileIn:

                # counter for if there is not enough stock in inventory, this is used for raising errors (i.e. we only have x in stock)
                stock_counter = 0

                invent_reader = csv.DictReader(csvfileIn, delimiter=',')
                
                for row in invent_reader:
                  # check if sold number has already reached 0 to prevent double lines.
                  if sold_number != 0:  
                    if product_name == row['Product_Name']:
                      found_product = True
                      batch = int(row['Count'])
                      stock_counter += batch
                      # check if there are more products to sell then there are in the current row & skip if there are nog more products of the id
                      if sold_number > batch and batch != 0:
                        row['Count'] = 0
                        sales_report_item[product_name][sale_num]["Total_Revenue"] += round(((float(row["Sell_Price"]) * batch)), 2)
                        sales_report_item[product_name][sale_num]["Total_Cost"] += round(batch * float(row["Price"]), 2)
                        sales_report_item[product_name][sale_num]["Total_Profit"] += round((batch * (float(row["Sell_Price"]) - float(row["Price"]))), 2)
                        sales_report_item[product_name][sale_num]["Sold_Product_Ids"][row["Id"]] = {
                          "amount_sold": batch,
                          "cost_price_each": row["Price"],
                          "sell_price_each": float(row["Sell_Price"]),
                          "total_cost": round(batch * float(row["Price"]), 2),
                          "total_profit": round(batch * (float(row["Sell_Price"]) - float(row["Price"])), 2)
                        }
                        # stock_counter.append(batch)
                        sold_number -= batch

                      elif sold_number < batch:
                        row['Count'] = batch - sold_number
                        sales_report_item[product_name][sale_num]["Total_Revenue"] += round((float(row["Sell_Price"]) * sold_number), 2)
                        sales_report_item[product_name][sale_num]["Total_Cost"] += round(sold_number * float(row["Price"]), 2)
                        sales_report_item[product_name][sale_num]["Total_Profit"] += round(sold_number * (float(row["Sell_Price"]) - float(row["Price"])), 2)
                        sales_report_item[product_name][sale_num]["Sold_Product_Ids"][row["Id"]] = {
                          "amount_sold": sold_number,
                          "cost_price_each": row["Price"],
                          "sell_price_each": float(row["Sell_Price"]),
                          "total_cost": round(sold_number * float(row["Price"]), 2),
                          "total_profit": round(sold_number * (float(row["Sell_Price"]) - float(row["Price"])), 2)
                        }
                        sold_number = 0
    
                  adjusted_rows.append(row)

              if sold_number > stock_counter:
                raise ValueError(f"\nWe have {sold_number} too few {product_name} in stock for this sale, we currently have {stock_counter}, this sale was not added")
              if found_product == False:
                raise ValueError(f"{product_name} not found, please add some to the inventory")

              # open inventory file and write adjusted lines
              with open(self.data_path, 'w+', newline='') as csvfileOut:
                invent_writer = csv.DictWriter(csvfileOut, self.invent_headers ,lineterminator="\n")
                invent_writer.writeheader()
                for row in adjusted_rows:
                  invent_writer.writerow(row)
              
              # open sales file and write the sales reports to it
              with open(self.sales_database_path, 'r+') as jsonfile:
                data = json.load(jsonfile)
                if not product_name in data:
                  data[product_name] = sales_report_item[product_name]
                else:
                  data[product_name][sale_num] = sales_report_item[product_name][sale_num]
                jsonfile.seek(0)
                json.dump(data, jsonfile, indent=4)
            
            return 1

          except ValueError as error:
            print(error)
            return 0
