import psycopg2
import random as r
import datetime as dt
import pymongo
from pymongo import MongoClient

PRODUCTS = "product"
INVENTORY = "inventory"
def connect_potsgres(database_name):
    """Connect to the PostgreSQL using psycopg2 with default database
       Return the connection"""
    conn = psycopg2.connect(database=database_name, user='postgres', password='admin', host='127.0.0.1', port= '5432')
    conn.autocommit = True
    print(conn)
    return conn

def create_product_table(conn):
    create_query = f"create table {PRODUCTS} (product_id SERIAL,name TEXT, description TEXT, date_created DATE NOT NULL,price INTEGER NOT NULL,quantity_available INTEGER NOT NULL DEFAULT 0,PRIMARY KEY (product_id))"
    cursor = conn.cursor()
    cursor.execute(create_query)
    print("Success!!")

def insert_query_products(conn):
    name = "Transistor"
    description = "NPN"
    date = str(dt.date.today())
    price = r.randint(50,100)
    quantity_available = r.randint(1,10)
    insert_query = f"Insert into {PRODUCTS} (name,description,date_created,price,quantity_available) values {name,description,date,price,quantity_available}"
    cursor = conn.cursor()
    cursor.execute(insert_query)
    search_product_id = f"select product_id from {PRODUCTS} where name = '{name}'"
    cursor.execute(search_product_id)
    product_id = cursor.fetchone()
    product_id = list(product_id)
    print("Success!!")
    disp_inventory(conn)
    insert_components(product_id[0])

def getCollection(db, collection):
    """Load feature descriptor collection from MongoDB"""
    client = MongoClient("mongodb://localhost:27017")
    return client[db][collection]

def create_inventory(conn):
    create_query = f"create table {INVENTORY} (component_id SERIAL,name TEXT, description TEXT, date_created DATE NOT NULL,price INTEGER NOT NULL,quantity_available INTEGER NOT NULL DEFAULT 0,PRIMARY KEY (component_id))"
    cursor = conn.cursor()
    cursor.execute(create_query)
    print("Success!!")

def insert_inventory(conn,name):
    description = "to make transistor"
    date = str(dt.date.today())
    price = 10
    quantity_available = r.randint(10,20)
    insert_query_inventory = f"Insert into {INVENTORY} (name,description,date_created,price,quantity_available) values {name,description,date,price,quantity_available}"
    cursor = conn.cursor()
    cursor.execute(insert_query_inventory)

def output(input_list):
    for i in range(0,len(input_list)):
        print(input_list[i],end='\n')
    
def disp_inventory(conn):
    cursor = conn.cursor()
    cursor.execute(f"select component_id,name from {INVENTORY}")
    component_data = cursor.fetchall()
    output(component_data)

def insert_components(product_id):
    product_collection = getCollection("The_Devils_Base", "product_collection")     
    components = []
    while True:
        component_id = input("Enter component ID (or type 'done' to finish): ")
        if component_id.lower() == 'done':
            break
        quantity = int(input("Enter quantity for given Component ID ({}): ".format(component_id)))
        components.append({"component_id": component_id, "quantity": quantity})
    
    product_data = {
    "product_id": product_id,
    "components": components,
    }
    # Insert data into the products collection
    product_collection.insert_one(product_data)

def add_suppliers(conn):
    supplier_collection = getCollection("The_Devils_Base", "supplier_collection")
    disp_inventory(conn)
    def get_next_supplier_id():
        max_order = supplier_collection.find_one(sort=[("supplier_id", pymongo.DESCENDING)])
        if max_order:
            return max_order["supplier_id"] + 1
        else:
            return 1
        
    components = []
    supplier_id = get_next_supplier_id()
    while True:
        component_id = input("Enter component ID (or type 'done' to finish): ")
        if component_id.lower() == 'done':
            break
        name = input("Enter the name of component: ")
        components.append({"component_id": component_id, "name": name})
    
    supplier_data = {
    "supplier_id": supplier_id,
    "components": components,
    }
    # Insert data into the products collection
    supplier_collection.insert_one(supplier_data)

if __name__ == '__main__':
    conn = connect_potsgres("group_project")
    # create_product_table(conn)
    # create_inventory(conn)
    # insert_inventory(conn,"emitter")
    # insert_inventory(conn,"base")
    # insert_inventory(conn,"diode")
    # disp_inventory(conn)
    # insert_query_products(conn)
    add_suppliers(conn)
    

    

    