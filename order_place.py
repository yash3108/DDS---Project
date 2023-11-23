import psycopg2
from NoSQL_data_handling import *
from network import *
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

def place_order(region):
    conn = get_database_connection(region)
    conn.autocommit = True
    customer_id = int(input("Enter Customer ID: "))
    query = f"SELECT COUNT(*) FROM your_customer_table WHERE customer_id = {customer_id};"
    cursor = conn.cursor
    row  = cursor.execute(query)
    count = row.fetchall()
    if count == 0:
        print("Customer ID does not exist")
        conn.close()
        return
    date = str(input("Enter date in YYYY-MM-DD format: "))
    display_products(conn)
    products = insert_order_data()
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

        query = f"INSERT INTO ORDERS (customer_id, order_date, status) VALUES ({customer_id}. {date}, 'Placed'));"
        cursor.execute(query)
        print("Order Placed: All products available for immediate delivery")
        insert_order(products)
        conn.close()
        return
    
    for product_id in rem_products:
        rem_components = {}
        client = getCollection(region, "product_collection")
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
            query = f"INSERT INTO ORDERS (customer_id, order_date, status) VALUES ({customer_id}. {date}, 'Components ordered'));"
            print("Order Placed: All Products are not available manufacturing remaining products from components available in warehouse")
            insert_order(products)
            conn.close()
            return
    collection = getCollection(region, "supplier_collection")
    for component_id in rem_components:
        query = f"SELECT component_name from Inventory where component_id = {component_id}"
        cursor.execute(query)
        component_name = cursor.fetchall()
        print(f"Missing component: {component_name} Quantity: {rem_components[component_id]}" )
        print("Suppliers for the component")
        result = collection.find({'components.component_id': component_id})
        for supplier in result:
            print(supplier)
        query = f"INSERT INTO ORDERS (customer_id, order_date, status) VALUES ({customer_id}. {date}, 'Not Placed: Missing Components'));"
        cursor.execute(query)
    conn.close()
        

                    


    
        
