#Inventory Management App
#Noemi Higashi

import csv
import os

def menu(username, products_count):
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Reset to the default products list.
        'Exit'    | Exit the program
    Please select an operation: """ # end of multi- line string. also using string interpolation

    return menu

def mini_menu (username, products_count):
    mini_menu = f"""
    -----------------------------------
    To continue, please select one of 'List', 'Show', 'Create', 'Update', 'Destroy', 'Reset'
    Or type 'Exit' to exit the program:

    """
    return mini_menu


#Initial Function
def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename) #reading some file (__file__) means the directory where the file belongs
    print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    products = []

    #TODO: open the file and populate the products list with product dictionaries

    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file) # special function Dictionary Reader
        for row in reader: #loop through the rows
            products.append (dict(row))
    return products

#Final Function
def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    print ("-----------------------------------")
    print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")
    #TODO: open the file and write a list of dictionaries. each dict should represent a product.

    with open(filepath, "w") as csv_file: #"w" means opening it for writing
        writer = csv.DictWriter(csv_file, fieldnames=["id","name","aisle","department","price"])
        writer.writeheader() # uses fieldnames set above to write a dictionary
        for p in products:
            writer.writerow(p)

def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    print (products)
    write_products_to_file(filename, products)

#Messages

message_list = ("""
-----------------------------------
LISTING PRODUCTS:
-----------------------------------
""")

message_show = ("""
-----------------------------------
SHOWING A PRODUCT:
-----------------------------------""")

message_create = ("""
-----------------------------------
CREATING A PRODUCT:
-----------------------------------""")

message_update = ("""
-----------------------------------
UPDATING A PRODUCT:
-----------------------------------""")

message_destroy = ("""
-----------------------------------
DESTROYING A PRODUCT:
-----------------------------------""")

message_reset = ("""
-----------------------------------
RESETING THE LIST
-----------------------------------
""")

def product_not_found():
    print("OOPS. Couldn't find a product with that identifier. Try listing products to see which ones exist.")

def product_price_not_valid():
    print(f"OOPS. That product price is not valid. Expecting a price like 4.99 or 0.77. Please try again.")

def is_valid_price(my_price):
    try:
        float(my_price)
        return True
    except Exception as e:
        return False


def run():
    # First, read products from file...
    products = read_products_from_file()

    type_name = input ("HELLO! TO START, TYPE YOUR NAME: ")
    print (type_name)
    # Then, prompt the user to select an operation...
    my_menu = (menu(username = type_name , products_count = len(products)))

    oper_name = input (my_menu)
    oper_name = oper_name.title()

    def operations ():

        if oper_name == "List":
            print (message_list)
            for p in products:
                print (str(p["id"]) + " - " + str(p["name"]))
            write_products_to_file(filename="products.csv", products=products)

        elif oper_name == "Show":
            print ("SHOWING A PRODUCT:")
            scan_id = int (input ("TYPE PRODUCT ID: "))
            if scan_id == None or scan_id > len(products): product_not_found()
            else:
                matching_id = [p for p in products if int(p["id"]) == scan_id]
                print (message_show)
                print (matching_id)
            write_products_to_file(products=products)

        elif oper_name == "Create":
            print ("CREATING A PRODUCT:")
            new_id = int (products[-1]["id"]) + 1

            new_name = str (input ("Ok. Please input product's name: "))
            new_aisle = str (input ("Ok. Please input product's aisle: "))
            new_dept = str (input ("Ok. Please input product's department: "))
            new_price = str (input ("Ok. Please input product's price: "))

            if is_valid_price(new_price) == False:
                product_price_not_valid()
                return

            new_product = {
                "id": new_id,
                "name": new_name,
                "aisle": new_aisle,
                "department": new_dept,
                "price": new_price
            }
            products.append(new_product)
            print (message_create)
            print (new_product)
            write_products_to_file(products=products)

        elif oper_name == "Update":
            print ("UPDATING A PRODUCT:")
            updt_id = int (input ("Ok. Please specify the product identifier: "))
            if updt_id == None or updt_id > len(products): product_not_found()

            old_name = [p["name"] for p in products if int(p["id"]) == updt_id]
            old_aisle = [p["aisle"] for p in products if int(p["id"]) == updt_id]
            old_dept = [p["department"] for p in products if int(p["id"]) == updt_id]
            old_price = [p["price"] for p in products if int(p["id"]) == updt_id]

            updt_name = str (input ("OK. New Product's Name (currently "+ str(old_name) + "): "))
            updt_aisle = str (input ("OK. New Product's Aisle (currently "+ str(old_aisle) + "): "))
            updt_dept = str (input ("OK. New Product's Department (currently "+ str(old_dept) + "): "))
            updt_price = str (input ("Ok. New Product's Price:  (currently "+ str(old_price) + "): "))

            if is_valid_price(updt_price) == False:
                product_price_not_valid()
                return

            updt_product = {
                "id": updt_id,
                "name": updt_name,
                "aisle": updt_aisle,
                "department": updt_dept,
                "price": updt_price
            }

            products [updt_id - 1] = updt_product
            print (message_update)
            print (updt_product)
            write_products_to_file(products=products)

        elif oper_name == "Destroy":
            print ("DELETING A PRODUCT:")
            del_id = int (input ("Type the Product ID: "))
            deleting_id = [p for p in products if int(p["id"]) == del_id]
            print (message_destroy)
            print (deleting_id)
            del products[del_id - 1]
            write_products_to_file(products=products)

        elif oper_name == "Reset":
            print (message_reset)
            reset_products_file ()


        elif oper_name == "Exit":
            print ("EXITING PROGRAM")

        else:
            print ("Unrecognized operation, please select one of 'List', 'Show', 'Create', 'Update', 'Destroy', 'Reset'")

    operations ()

    while True:
        my_mini_menu = (mini_menu(username = type_name , products_count = len(products)))
        oper_name = input (my_mini_menu)
        oper_name = oper_name.title()
        operations ()
        if oper_name == "Exit":
            break



# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__":
    run()
