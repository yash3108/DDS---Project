import psycopg2
from NoSQL_data_handling import *
def display_products(conn): 
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Define the SQL query to select product name and price from the product table
    query = "SELECT product_name, price FROM product"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Display the product information
    for row in rows:
        product_name, price = row
        print(f"Product N: {product_name}, Price: {price}")

def get_connection(region):
    return conn

def place_order(conn):
    display_products(conn)
    products = insert_order()
    rem_products = {}
    for product_id in products:
        query = f"SELECT quantity from product where product_id = '{product_id}'",
        cursor = conn.cursor()
        cursor.execute(query)
        available_qty = cursor.fetchall()
        if products[product_id] <= available_qty:
            continue
        else:
            rem_products[product_id] = products[product_id] - available_qty
        
    if not len(rem_products):
        query = "INSERT INTO ORDERS (customer_id, order_date, status) VALUES ())"
        
        print("Order Placed: All products available for immediate delivery")
        return
    
    for product_id in rem_products:
        rem_components = {}
        client = getCollection(region_db, "product_collection")
        components = get_product_components(client, product_id)
        for component_id in components:
            query = f"SELECT quantity from inventory where component_id = '{component_id}'"
            cursor.execute(query)
            available_qty = cursor.fetchall()
            if components[component_id] <= available_qty:
                continue
            else:
                rem_components[component_id] = components[component_id] - available_qty
        if not len(rem_components):
            print("Order Placed: All Products are not available manufacturing remaining products from components available in warehouse")
            return
    collection = getCollection(region_db, "supplier_collection")
    for component_id in rem_components:
        query = f"SELECT component_name from Inventory where component_id = {component_id}"
        cursor.execute(query)
        component_name = cursor.fetchall()
        print(f"Missing component: {component_name} Quantity: {rem_components[component_id]}" )
        print("Suppliers for the component")
        result = collection.find({'components.component_id': component_id})
        for supplier in result:
            print(supplier)
        

                    


    
        
