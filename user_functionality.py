import psycopg2
import random as r
import datetime as dt
from NoSQL_data_handling import *
from network import *

PRODUCTS = "Products"
INVENTORY = "Inventory"

def local_user_menu(lv_region_index):
    conn = get_database_connection(gv_regions[lv_region_index])
    print("\Select Options:")
    print("\n1. Add Product")
    print("\n2. Add Supplier")
    print("\n3. Add Components")
    print("\n4. Restock Inventory")
    print("\n5. Exit")
    local_user_input = int(input("\nEnter choice number: "))
    
    if local_user_input == 1:
        insert_products_inventory(conn,lv_region_index)
    elif local_user_input == 2:
        add_suppliers(conn,lv_region_index)
    elif local_user_input == 3:
        add_component_inventory(conn)
    elif local_user_input == 4:
        restock_inventory(conn)  
    else:
        close_system() 

    local_user_menu(lv_region_index,conn)

def insert_products_inventory(conn,lv_region_index):
    '''
    This function adds new product into Products table.
    '''
    name = input("Enter Product name: ")
    description = input("Enter Product Description: ")
    date = str(dt.date.today())
    price = int(input("Enter Products Price:$ "))
    quantity_available = int(input("Enter Initial Quantity: "))
    insert_query = f"Insert into {PRODUCTS} (name,description,date_created,price,quantity) values {name,description,date,price,quantity_available}"
    cursor = conn.cursor()
    cursor.execute(insert_query)
    search_product_id = f"select product_id from {PRODUCTS} where name = '{name}'"
    cursor.execute(search_product_id)
    product_id = cursor.fetchone()
    product_id = list(product_id)
    print("Inventory: \n")
    display_inventory(conn)
    while True:
           response = input("Do you want to Insert new Components? (Yes/No): ")
           if response == "Yes":
               add_component_inventory(conn)
           else:
               break
    component_list = []
    search_component_id = f"select component_id from {INVENTORY}"
    cursor.execute(search_component_id)
    get_component_list = cursor.fetchall()
    for i in range(0,len(get_component_list)):
        component_list.append(list(get_component_list[i])[0])
        
    print("Inventory: ")
    display_inventory(conn)
    print("-------Product Component Mapping-------")
    insert_product_components(lv_region_index,product_id[0],component_list)
    cursor.close()

def output(input_list):
    for i in range(0,len(input_list)):
        print(input_list[i])
    
def display_inventory(conn):
    cursor = conn.cursor()
    cursor.execute(f"select component_id,name,quantity from {INVENTORY}")
    component_data = cursor.fetchall()
    output(component_data)
    cursor.close()
    
def insert_product_components(lv_region_index,product_id,component_list):
    region_db = gv_regions[lv_region_index]
    region_db+="_db"
    product_collection = getCollection(region_db, "product_collection")     
    components = insert_new_components(component_list)
    product_data = {
    "product_id": product_id,
    "components": components,
    }
    # Insert data into the products collection
    product_collection.insert_one(product_data)

def add_suppliers(conn,lv_region_index):
    '''
    This function adds a new supplier in our NO-SQL database
    '''
    display_inventory(conn)
    region_db = gv_regions[lv_region_index]
    region_db+="_db"
    supplier_collection = getCollection(region_db, "supplier_collection")
    supplier_id,name,components = insert_supplier_components(region_db)
    supplier_data = {
    "supplier_id": supplier_id,
    "supplier_name": name,
    "components": components,
    }
    # Insert data into the suppliers collection
    supplier_collection.insert_one(supplier_data)
 
def add_component_inventory(conn):
    '''
    This function adds new components into our Inventory
    '''
    name = input("Enter name of new Component: ")
    description = input("Enter description on new Component: ")
    date = str(dt.date.today())
    price = int(input("Enter thr price of new Component:$ "))
    quantity_available = int(input("Enter the Initial Quantity: "))
    insert_query_inventory = f"Insert into {INVENTORY} (name,description,date_created,price,quantity) values {name,description,date,price,quantity_available}"
    cursor = conn.cursor()
    cursor.execute(insert_query_inventory)

    display_inventory(conn)
    cursor.close()
    
def restock_inventory(conn):
    '''
    This function restocks our Inventory 
    '''
    display_inventory(conn)
    cursor = conn.cursor()
    while True:
        component_id = input("Enter component ID (or type 'done' to finish): ")
        if component_id.lower() == 'done':
            break
        search_query = f"SELECT quantity from {INVENTORY} where component_id = {component_id}"
        cursor.execute(search_query)
        answer = cursor.fetchone()
        current_quantity = list(answer)[0]
        print("Current Stock of that component: ",current_quantity)
        new_quantity = int(input("Enter how much units you want to add: "))
        total_quantity = current_quantity+new_quantity
        update_query = f"UPDATE {INVENTORY} SET quantity = {total_quantity} where component_id = {component_id}"
        cursor.execute(update_query)
    
    cursor.close()
    print("Inventory after Restocking: ")
    display_inventory(conn)