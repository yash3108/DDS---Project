from network import *

create_client()
check_network_connection()
initialize_containers()
check_database_connection()

def init_menu():
    """
    Input: NA
    Output: user input
    """
    print("\Select User:")
    print("\n1. Admin")
    print("\n2. Local User")
    print("\n3. Customer")
    re_u_input = int(input("\nEnter choice number: "))

    return re_u_input

def region_menu():
    """
    Input: NA
    Output: user region
    """
    print("\nSelect your region:")
    for i in range(len(gv_regions) - 1):
        print(f"\n{i+1}. {gv_regions[i]}")
    u_input = int(input("\nEnter choice number: "))
    return gv_regions[u_input - 1]

def admin_menu():
    pass

def local_user_menu():
    pass

def customer_menu():
    pass

def navigate(im_u_input):
    """
    Input: user input
    Output: NA
    """
    match im_u_input:
        case 1:
            admin_menu()
        case 2:
            local_user_menu()
        case 3:
            customer_menu()

region_menu()