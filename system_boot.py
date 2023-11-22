from network import *
from init_app import *
from setup_db import *

create_client()
check_network_connection()
initialize_containers()
check_database_connection()
init_app()
setup_db()