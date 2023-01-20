# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint 
SCOPE= [
    "https://www.googleapis.com/auth/spreadsheets",
     "https://www.googleapis.com/auth/drive.file",
      "https://www.googleapis.com/auth/drive"
]

CREDS= Credentials.from_service_account_file('creds.json')
SCOPED_CREDS=CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT=gspread.authorize(SCOPED_CREDS)
SHEET=GSPREAD_CLIENT.open('love_sandwiches')

"""
sales=SHEET.worksheet('sales')
data=sales.get_all_values()

print(data)
"""

def get_sales_data():
    """
    Get sales figures input from the user
    """
    while True:

        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print ("example: 10,20,30,40,50,60\n")

        data_str=input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break
    print(sales_data)
    return sales_data    
 
def validate_data(values):
    """ 
    Inside the try, converts all string values into integers.
    Raises ValueError if string cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values)!=6:
            raise ValueError (f"Exactly 6 values required, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False 
    return True     

def update_sales_worksheet(data):
    """
    Update sales worksheet, add now eow with the list data provided.
    """
    print("Updating sales worksheet ...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each iten type.

    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    pprint(stock)
    stock_row = stock[-1]

    #print(f"stock row: {stock_row}")
    #print(f"sales row: {sales_row}")

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock)-sales
        surplus_data.append(surplus)
   # print(surplus_data)
    return surplus_data

def get_last_5_entries_sales():
    """
    Colect collums of data from sales worksheet, collecting 
    the last entries for each sandwich and return the data
    as a list of lists. 
    """
    sales=SHEET.worksheet("sales")
    #column = sales.col_values(3)
    #print(column)
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    pprint(columns)
    
    






def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add now eow with the list data provided.
    """
    print("Updating surplus worksheet ...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):

    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")    

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    print(data)
    sales_data=[int(num) for num in data]
   # update_sales_worksheet(sales_data)
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    #update_surplus_worksheet(new_surplus_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welcome to Love Sandwiches Data Automation")
# main()

get_last_5_entries_sales()
