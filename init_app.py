from network import *
from user_functionality import *
# Function to initialize the app menu
def init_menu():
    """
    Input: NA
    Output: user input
    """
    print("\Select User:")
    print("\n1. Admin")
    print("\n2. Local User")
    print("\n3. Customer")
    print("\n4. Exit")
    re_u_input = int(input("\nEnter choice number: "))

    return re_u_input

# Function to get region input
def region_menu():
    """
    Input: NA
    Output: user region index
    """
    print("\nSelect your region:")
    for i in range(len(gv_regions) - 1):
        print(f"\n{i+1}. {gv_regions[i]}")
    u_input = int(input("\nEnter choice number: "))
    return (u_input - 1)

def admin_menu():
    pass

def local_user_menu(im_region_index):
    pass

def customer_menu(im_region_index):
    pass

# Funtion to navigate based on user input
def navigate(im_u_input):
    """
    Input: user input
    Output: NA
    """
    if im_u_input:
        if im_u_input == 1:
            admin_menu()
        elif im_u_input == 2:
            lv_region_index = region_menu()
            local_user_menu(lv_region_index)
        elif im_u_input == 3:
            lv_region_index = region_menu()
            customer_menu(lv_region_index)
        else:
            close_system()

# Function to start the app
def init_app():
    """
    Input: NA
    Output: NA
    """
    lv_u_input = init_menu()
    navigate(lv_u_input)
