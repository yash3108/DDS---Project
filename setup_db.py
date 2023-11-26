from init_app import *
import json
import time

def initialize_data_nosql(region):

    if region == gv_regions[3]:
        file = 'initialize_nosql_central.json'
        try:
            with open(file, 'r') as file:
                data = json.load(file)
            region_db = region+"_db"
            collection = getCollection(region_db, "order_collection")
            collection.insert_many(data)
            print("Mapped Orders to products")
        except Exception as e:
            print(f"Error: {e}")
    else:
        file = f'initialize_nosql_product_{region}.json'
        try:
            with open(file, 'r') as file:
                data = json.load(file)
            region_db = region+"_db"
            collection = getCollection(region_db, "product_collection")
            collection.insert_many(data)
            print("Mapped Products to Components")
        except Exception as e:
            print(f"Error: {e}")

        try:
            file = f'initialize_nosql_supplier_{region}.json'
            with open(file, 'r') as file:
                data = json.load(file)
            region_db = region+"_db"
            collection = getCollection(region_db, "supplier_collection")
            collection.insert_many(data)
            print("Added Suppliers for Components")
        except Exception as e:
            print(f"Error: {e}")

def display_inserted_data():
    for region in gv_regions:
        conn = get_database_connection(region)
        region_db = region+"_db"
        cursor = conn.cursor()
        if region == gv_regions[3]:
            query = "Select * from Customers;"
            cursor.execute(query)
            rows = cursor.fetchall()
            print("\nCustomers")
            for row in rows:
                print(row)
            query = "Select * from Orders;"
            cursor.execute(query)
            rows = cursor.fetchall()
            print("\nOrders")
            for row in rows:
                print(row)
            collection = getCollection(region_db, "order_collection")
            results = collection.find()
            print("\nOrder Mapping")
            for result in results:
                print(result)
        else:
            print(f"\nProducts in {region}")
            query = "Select * from Products;"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
            print(f"\nInventory in {region}")
            query = "Select * from Inventory;"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row) 
            collection = getCollection(region_db, "product_collection")
            results = collection.find()
            print("\nProduct Mapping")
            for result in results:
                print(result) 
            collection = getCollection(region_db, "supplier_collection") 
            results = collection.find()
            print("\nSupplier Mapping")
            for result in results:
                print(result) 


def setup_db():
    # Setup local DBs
    for region in gv_regions:
        conn = get_database_connection(region)
        conn.autocommit = True
        cursor = conn.cursor()
        if region == "central":
            sql_script_path = 'create_script_central.sql'
        else:
            # Specify the path to your SQL script
            sql_script_path = 'create_script_local.sql'

        # Read the SQL script
        with open(sql_script_path, 'r') as script_file:
            sql_script = script_file.read()
        try:
            cursor.execute(sql_script)
            print(f"Create DB Script executed successfully for {region} DB")
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()
    
    for region in gv_regions:
        conn = get_database_connection(region)
        conn.autocommit = True
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM orders;"
        cursor = conn.cursor()
        cursor.execute(query)
        count = cursor.fetchall()
        count = count[0][0]
        if count == 0:
            sql_script_path = f'initialize_data_{region}.sql'
            with open(sql_script_path, 'r') as script_file:
                sql_script = script_file.read()
            try:
                cursor.execute(sql_script)
                print(f"Insert data Script executed successfully for {region} DB")
                initialize_data_nosql(region)
            except Exception as e:
                conn.rollback()
                print(f"Error: {e}")    
            
        # Close the cursor and connection
        cursor.close()
        conn.close()
    display_inserted_data()



