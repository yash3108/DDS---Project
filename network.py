import docker
import psycopg2

global gv_client, gv_network
gv_client, gv_network = None, None
gv_network_name = "dds_network"
gv_postgres_user = 'postgres'
gv_postgres_password = "password"
gv_default_database_credentials = {"dbname": "postgres", 
                                   "user": "postgres", 
                                   "password": "postgres"}
gv_regions = ["boston", 
              "denver", 
              "seattle", 
              "central"]

# Function to create docker client
def create_client():
    """
    Input: NA
    Output: NA
    """
    global gv_client
    gv_client = docker.from_env()
    print("Client created successfully")

# Function to create network in docker
def create_network(im_network_name):
    """
    Input: network name
    Output: NA
    """
    global gv_client, gv_network
    gv_network = gv_client.networks.create(im_network_name, driver="bridge")
    print("Network created successfully")

# Function to check network connection
def check_network_connection():
    """
    Input: NA
    Output: NA
    """
    check_flag = False
    if gv_client:
        lv_current_networks = gv_client.networks.list()

        for network in lv_current_networks:
            if network.name == gv_network_name:
                check_flag = True
                print("Network check successful: Network is active")
                break
        if not check_flag:
            print("Network check successful: Network is inactive")
            print("Creating network")
            create_network(gv_network_name)
    else:
        create_client()
        create_network(gv_network_name)
        
# Function to create postgres container in docker
def create_postgres_container(im_container_name):
    """
    Input: container name
    Output: container object
    """
    re_postgres_container = gv_client.containers.run(
        "postgres",
        name=im_container_name,
        detach=True,
        environment={
            'POSTGRES_USER': gv_postgres_user,
            "POSTGRES_PASSWORD": gv_postgres_password},
        network=gv_network_name
    )

    print(f"{im_container_name} container created")

    return re_postgres_container

# Function to check if container is running
def is_container_running(im_container_name):
    if gv_client:
        lv_containers = gv_client.containers.list(all=True)
        
        for container in lv_containers:
            if container.name == im_container_name:
                return container.status == 'running'
            
        print(f"{im_container_name} not present")
        return False
    else:
        create_client()
        is_container_running(im_container_name)

# Function to check if container is present
def is_container_present(im_container_name):
    lv_containers = gv_client.containers.list(all=True)

    for container in lv_containers:
        if container.name == im_container_name:
            return True
    return False

# Function to initialize docker containers
def initialize_containers():
    """
    Input: NA
    Output: NA
    """
    for region in gv_regions:
        lv_container_name = region + "_container"

        if is_container_running(lv_container_name):
            print(f"{lv_container_name} is running")
        elif is_container_present(lv_container_name):
            lv_container = gv_client.containers.get(lv_container_name)
            # Start the container if it's stopped
            if lv_container.status == 'exited':
                lv_container.start()
                print(f"{lv_container_name} started")
            else:
                print(f"{lv_container_name} is running")
        else:
            create_postgres_container(lv_container_name)

# Function to get default database connection
def get_default_database_connection(im_container_name):
    container = gv_client.containers.get(im_container_name)
    ip_address = container.attrs['NetworkSettings']['IPAddress']

    conn = psycopg2.connect(
        dbname=gv_default_database_credentials["dbname"],
        user=gv_default_database_credentials["user"],
        password=gv_default_database_credentials["password"],
        host=ip_address,
    )
    conn.autocommit = True
    return conn

# Function to create a database in a container
def create_database(conn, im_dbname):
    """
    Input: databse connection, Database Name
    Output: NA
    """
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE {im_dbname};")
    cursor.close()
    conn.close()
    print(f"{im_dbname} created successfully")

# Function to check databse connection
def check_database_connection():
    """
    Input: NA
    Output: NA
    """
    for region in gv_regions:
        lv_container_name = region + "_container"
        lv_dbname = region + "_db"

        conn = get_default_database_connection(lv_container_name)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (lv_dbname,))
        exists = bool(cursor.rowcount)

        if exists:
            print(f"{lv_dbname} connection test successful")
        else:
            create_database(conn, lv_dbname)

# Function to get database connection
def get_database_connection(im_region):
    """
    Input: region
    Output: databse connection
    """
    lv_container_name = im_region + "_container"
    lv_db_name = im_region + "_db"

    container = gv_client.containers.get(lv_container_name)
    ip_address = container.attrs['NetworkSettings']['IPAddress']

    conn = psycopg2.connect(
        dbname=lv_db_name,
        user=gv_default_database_credentials["user"],
        password=gv_default_database_credentials["password"],
        host=ip_address,
    )
    conn.autocommit = True
    return conn

# Function to stop running docker container
def stop_container(im_container_name):
    """
    Input: container name
    Output: NA
    """
    container = gv_client.containers.get(im_container_name)
    # Check if the container is running and then stop it
    if container.status == 'running':
        container.stop()
        print(f"{im_container_name} stopped")
    else:
        return False

# Function to close the system
def close_system():
    """
    Input: NA
    Output: NA
    """
    for region in gv_regions:
        lv_container_name = region + "_container"
        stop_container(lv_container_name)
    print("\nSystem closed")