import os
import csv
import json
import pytest
import datetime
from product_inventory import Inventory

@pytest.fixture
def buying_product():
    bought_product = [{
        "Product_Name": "Apple",
        "Product_Group": "Fruit",
        "Count": 500,
        "Initial_Count": 0,
        "Price": 0.25,
        "Markup": 1.25, 
        "Expiration_Date": datetime.date.today() + datetime.timedelta(25),
        "Date_Product_Added": datetime.datetime.now()
    }]
    return bought_product

@pytest.fixture
def selling_product():
    sold_product = [{
        "name": "Apple",
        "amount": 30
    }]
    return sold_product

@pytest.fixture
def multiple_products():
        product_list = [
            {
                "Product_Name": "Kiwi",
                "Product_Group": "Fruit",
                "Count": 200,
                "Initial_Count": "",
                "Price": 0.45,
                "Markup": 1.35, 
                "Expiration_Date": datetime.date.today() + datetime.timedelta(35),
                "Date_Product_Added": datetime.datetime.now()
            },
            {
                "Product_Name": "Steak",
                "Product_Group": "Meat",
                "Count": 50,
                "Initial_Count": "",
                "Price": 2.25,
                "Markup": 2.00, 
                "Expiration_Date": datetime.date.today() + datetime.timedelta(12),
                "Date_Product_Added": datetime.datetime.now()
            },
            {
                "Product_Name": "Kiwi",
                "Product_Group": "Fruit",
                "Count": 100,
                "Initial_Count": "",
                "Price": 0.45,
                "Markup": 1.35, 
                "Expiration_Date": datetime.date.today() + datetime.timedelta(35),
                "Date_Product_Added": datetime.datetime.now()
            }
        ]
        return product_list

@pytest.fixture
def selling_multiple_products():
        sold_products = [
            {
                "name": "Kiwi",
                "amount": 25
            },
            {
                "name": "Kiwi",
                "amount": 135
            },
            {
                "name": "Kiwi",
                "amount": 75
            },
            {
                "name": "Kiwi",
                "amount": 25
            },
        ]
        return sold_products




def test_product_inventory(buying_product, selling_product, multiple_products, selling_multiple_products):
    try:
        # Arrange
        cur_dir = os.getcwd()
        test_file_path = f"{cur_dir}/test_Inventory.csv"
        test_file_sales_path = f"{cur_dir}/test_sales.json"
        open(test_file_path, 'x')
        with open(test_file_sales_path, 'w+') as testjson:
            json.dump({}, testjson)
            

        test_invent = Inventory(test_file_path, test_file_sales_path,"./Uploads/Template/Upload_Form.csv", 
        "./Uploads/Template/Sales_Upload_Form.csv", date_adjust=0)
        test_invent.add_product(buying_product)
        test_invent.sell_products(selling_product)
        test_invent.add_product(multiple_products)
        test_invent.sell_products(selling_multiple_products)


        # check if all needed headers for buying products are still created
        assert set(buying_product[0].keys()).issubset(set(test_invent.invent_headers)) == True

        # read and test the created/adjusted inventory file
        with open(test_file_path, 'r', newline='') as csvFile:
            csv_reader = csv.DictReader(csvFile)
            # test if created headers in csv file are the same as the hardcoded file in the class
            assert csv_reader.fieldnames == test_invent.invent_headers

            # empty list to store/check unique product ids
            id_list = []

            for row in csv_reader:
                print(row)
                if row["Product_Name"] == buying_product[0]["Product_Name"]:
                    # test if all fields in file have values
                    for item in row:
                        assert len(row[item]) != 0
                    # test sell price
                    assert float(row["Sell_Price"]) == round(buying_product[0]["Price"] * buying_product[0]["Markup"], 2)

                if row["Product_Name"] == "Kiwi":
                    # test if the count of the product that is sold is running to 0 is correctly processed
                    assert int(row["Count"]) == 0 or int(row["Count"]) == 40

                # test unique ids
                assert row["Id"] not in id_list
                id_list.append(row["Id"])

        # read and test the created sales file
        with open(test_file_sales_path, 'r') as sales_file:
            data = json.load(sales_file)
            for prod in ["Apple", "Kiwi"]:
                assert prod in list(data.keys())

    # remove test file
    finally:
        # print("Test")
        os.remove(test_file_path)
        os.remove(test_file_sales_path)
    


