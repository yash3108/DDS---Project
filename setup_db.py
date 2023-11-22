from init_app import *

def setup_db():
    # Setup local DBs
    for region in gv_regions:
        conn = get_database_connection(region)
        conn.autocommit = True
        cursor = conn.cursor
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
            print("Local DB Script executed successfully")
        except Exception as e:
            conn.rollback()
            print(f"Error: {e}")
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

