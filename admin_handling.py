from network import *
from user_functionality import *
import init_app

def admin_menu():
    option = int(input("Select Option : \n1. Access Central DB Fucntions\n2. Access Local DB Functions\n"))
    match option:
        case 1:
            central_db_functions()
        case 2:
            region = init_app.region_menu()
            local_user_menu(region - 1)
        case _:
            print("Slect the appropriate option")

def central_db_functions():
    conn = get_database_connection(gv_regions[3])
    conn.autocommit = True 
    cursor = conn.cursor()
    func = int(input("Select from below Functions\n1. Add New Customer\n2. Display Sales\n"))
    match func:
        case 1:
            name = str(input("Enter Customer Name"))
            country = str(input("Enter your Country"))
            region =  int(input("Select closest Region: \n1. Boston\n2. Denver\n3. Seattle\n"))
            region = gv_regions[region - 1]
            query = f"INSERT INTO Customers (name, country, region) VALUES {name,country,region};"
            cursor.execute(query)
        case 2:
            year = int(input("Enter year to display Sales: "))
            query = f"SELECT * FROM Orders WHERE EXTRACT (YEAR FROM order_date) = {year};"
            cursor.execute(query)
            results = cursor.fetchall()
            for result in results:
                print(result)
        case _:
            print("Select appropriate function")
        
    conn.close()
