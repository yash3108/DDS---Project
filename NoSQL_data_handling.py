import pymongo
from pymongo import MongoClient

def getCollection(db, collection):
    """Load feature descriptor collection from MongoDB"""
    client = MongoClient("mongodb://localhost:27017")
    return client[db][collection]


def get_order(order_collection, order_id):
    # order_collection = getCollection("The_Devils_Base", "order_collection")
    order = order_collection.find_one({"order_id": order_id})
    return order


def get_product_components(region_db, product_id):
    product_collection = getCollection(region_db, "product_collection")
    product = product_collection.find_one({"product_id": product_id})
    return product["components"]

def insert_order_data():
    
    products = []
    while True:
        product_id = input("Enter product ID to add in cart(or type 'done' to finish): ")
        if product_id.lower() == 'done':
            break
        quantity = int(input("Enter quantity for the Product ID ({}): ".format(product_id)))
        products.append({"product_id": product_id, "quantity": quantity})
    return products

def insert_order(region_db, products):
    order_collection = getCollection(region_db, "order_collection")
    def get_next_order_id():
        max_order = order_collection.find_one(sort=[("order_id", pymongo.DESCENDING)])
        if max_order:
            return max_order["order_id"] + 1
        else:
            return 1
    order_data = {
    "order_id": get_next_order_id(),
    "products": products,
    }
    # Insert data into the orders collection
    order_collection.insert_one(order_data)

def insert_new_components(component_list):
    components = []
    while True:
        component_id = input("Enter component ID (or type 'done' to finish): ")
        if component_id.lower() == 'done':
            break
        if int(component_id) not in component_list:
            print("***This Component doesn't exists in the Inventory***")
        else:
            quantity = int(input("Enter quantity for given Component ID ({}): ".format(component_id)))
            components.append({"component_id": component_id, "quantity": quantity})

    return components

def insert_supplier_components(region_db):
    supplier_collection = getCollection(region_db, "supplier_collection")
    def get_next_supplier_id():
        max_order = supplier_collection.find_one(sort=[("supplier_id", pymongo.DESCENDING)])
        if max_order:
            return max_order["supplier_id"] + 1
        else:
            return 1
        
    components = []
    supplier_id = get_next_supplier_id()
    supplier_name = input("Enter Suppliers name: ")
    while True:
        component_id = input("Enter component ID (or type 'done' to finish): ")
        if component_id.lower() == 'done':
            break
        name = input("Enter the name of component: ")
        components.append({"component_id": component_id, "name": name})
    
    return supplier_id,supplier_name,components