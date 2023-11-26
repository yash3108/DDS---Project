import psycopg2
from NoSQL_data_handling import *
from network import *

def display_products(conn): 
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Define the SQL query to select product name and price from the product table
    query = "SELECT name, price FROM products;"

    # Execute the query
    cursor.execute(query)

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Display the product information
    for row in rows:
        product_name, price = row
        print(f"Product N: {product_name}, Price: {price}")

def customer_menu(region):
    region_db = region + "_db"
    conn_central = get_database_connection(gv_regions[3])
    conn_central.autocommit = True
    customer_id = int(input("Enter Customer ID: "))
    query = f"SELECT COUNT(*) FROM customers WHERE customer_id = {customer_id};"
    cursor_central = conn_central.cursor()
    cursor_central.execute(query)
    count = cursor_central.fetchall()
    count = count[0][0]
    if count == 0:
        print("Customer ID does not exist")
        conn_central.close()
        return
    date = str(input("Enter date in YYYY-MM-DD format: "))
    conn = get_database_connection(region)
    display_products(conn)
    products = insert_order_data()
    rem_products = {}
    available_products = []
    for i in range(len(products)):
        print(products[i]['product_id'])
        query = f"SELECT quantity from products where product_id = {products[i]['product_id']};"
        cursor = conn.cursor()
        cursor.execute(query)
        available_qty = cursor.fetchall()
        available_qty = available_qty[0][0]
        available_products.append(available_qty)
        if int(products[i]['quantity']) <= available_qty:
            continue
        else:
            rem_products[products[i]['product_id']] = products[i]['quantity'] - available_qty
    if not len(rem_products):
        for i in range(len(products)):
            updated_quantity = available_products[i] - products[i]['quantity']
            query = f"UPDATE Products SET quantity = {updated_quantity} where product_id = {products[i]['product_id']}"
            cursor.execute(query)
        order_status = 'Placed'
        query = f"INSERT INTO ORDERS (customer_id, order_date, status, region) VALUES {customer_id, date, order_status, region};"
        cursor_central.execute(query)
        print("Order Placed: All products available for immediate delivery")
        insert_order("central_db", products)
        conn.close()
        conn_central.close()
        return
    
    for product_id in rem_products:
        rem_components = []
        components = get_product_components(region_db, int(product_id))
        
        for component in components:
            query = f"SELECT quantity from inventory where component_id = '{component['component_id']}'"
            cursor.execute(query)
            available_qty = cursor.fetchall()
            available_qty = available_qty[0][0]
            conn.autocommit = False
            if component['quantity']*rem_products[product_id] <= available_qty:
                updated_comp_quantity = available_qty - component['quantity']*rem_products[product_id]
                query = f"UPDATE Inventory SET quantity = {updated_comp_quantity} where component_id = {int(component['component_id'])}"
                cursor.execute(query)
                continue
            else:
                rem_components.append(int(component['component_id']))

        if not len(rem_components):
            conn.commit()
            conn.autocommit = True
            for i in range(len(products)):
                updated_quantity = available_products[i] - products[i]['quantity']
                if updated_quantity < 0:
                    updated_quantity = 0
                query = f"UPDATE Products SET quantity = {updated_quantity} where product_id = {products[i]['product_id']}"
                cursor.execute(query)
            order_status = 'Manufacturing in process'
            query = f"INSERT INTO ORDERS (customer_id, order_date, status, region) VALUES {customer_id, date, order_status, region};"
            cursor_central.execute(query)
            print("Order Placed: All Products are not available manufacturing remaining products from components available in warehouse")
            insert_order("central_db", products)
            conn.close()
            conn_central.close()
            return
    supplier_collection = getCollection(region_db, "supplier_collection")
    for component_id in rem_components:
        query = f"SELECT name from Inventory where component_id = {component_id}"
        cursor.execute(query)
        component_name = cursor.fetchall()
        component_name = component_name[0][0]
        print(f"Missing component: {component_name}" )
        print("Suppliers for the component")
        result = supplier_collection.find({'components.component_id': str(component_id)})
        for supplier in result:
            print(supplier)
    conn.close()
        

                    


    
        
