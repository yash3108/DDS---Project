import pymongo
from pymongo import MongoClient

def getCollection(db, collection):
    """Load feature descriptor collection from MongoDB"""
    client = MongoClient("mongodb://localhost:27017")
    return client[db][collection]

def show_order(order_id):
    order_collection = getCollection("The_Devils_Base", "order_collection")
    order = order_collection.find_one({"order_id": order_id})
    print(order)

def get_order(order_collection, order_id):
    # order_collection = getCollection("The_Devils_Base", "order_collection")
    order = order_collection.find_one({"order_id": order_id})
    return order

def show_product_components(product_id):
    product_collection = getCollection("The_Devils_Base", "product_collection")
    product = product_collection.find_one({"product_id": product_id})
    print(product)

def get_product_components(product_collection, product_id):
    product = product_collection.find_one({"product_id": product_id})
    return product["components"]

def insert_order():
    order_collection = getCollection("The_Devils_Base", "order_collection")
    def get_next_order_id():
        max_order = order_collection.find_one(sort=[("order_id", pymongo.DESCENDING)])
        if max_order:
            return max_order["order_id"] + 1
        else:
            return 1
        
    products = []
    while True:
        product_id = input("Enter product ID (or type 'done' to finish): ")
        if product_id.lower() == 'done':
            break
        quantity = int(input("Enter quantity for given Product ID ({}): ".format(product_id)))
        products.append({"product_id": product_id, "quantity": quantity})
    
    order_data = {
    "order_id": get_next_order_id(),
    "products": products,
    }
    # Insert data into the orders collection
    order_collection.insert_one(order_data)
    return products

def insert_product():
    product_collection = getCollection("The_Devils_Base", "product_collection")
    def get_next_product_id():
        max_order = product_collection.find_one(sort=[("product_id", pymongo.DESCENDING)])
        if max_order:
            return max_order["product_id"] + 1
        else:
            return 1
        
    components = []
    while True:
        component_id = input("Enter component ID (or type 'done' to finish): ")
        if component_id.lower() == 'done':
            break
        quantity = int(input("Enter quantity for given Component ID ({}): ".format(component_id)))
        components.append({"component_id": component_id, "quantity": quantity})
    
    product_data = {
    "product_id": get_next_product_id(),
    "components": components,
    }
    # Insert data into the products collection
    product_collection.insert_one(product_data)

def insert_new_components(component_list):
    components = []
    while True:
        component_id = input("Enter component ID (or type 'done' to finish): ")
        if component_id.lower() == 'done':
            break
        if int(component_id) not in component_list:
            print("This Component doesn't exists in the Inventory: ")
            break
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
    while True:
        component_id = input("Enter component ID (or type 'done' to finish): ")
        if component_id.lower() == 'done':
            break
        name = input("Enter the name of component: ")
        components.append({"component_id": component_id, "name": name})
    
    return supplier_id,components