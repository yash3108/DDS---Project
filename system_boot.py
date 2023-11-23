from network import *
from init_app import *
from setup_db import *

create_client()
check_network_connection()
initialize_containers()
check_database_connection()
setup_db()
init_app()