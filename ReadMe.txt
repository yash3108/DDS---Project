Software Requirements:
1. Docker Desktop
2. Python v3.7 and above
3. Python Interpreter(VS code preferred)
4. PosgreSQL
5. MongoDB Client
6. MongoDB Compass

*******************************************************
NOTE :
- The whole code is available in the "The_Devil's_Base_Package"
- Keep all files in one folder
- Please run the run.bat file only to execute the project.

*******************************************************

-----------------PART1----------------
Database and Table creation, Data Insertion and Displaying inserted data

1. run the 'run.bat' file in the terminal
2. Initializing Program and Scripts will run and inserted data will be displayed on the terminal

-----------------PART2----------------
Data Fragmentation based on region

1. Open the Customer Profile
2. Select the products to be ordered and enter their quantity
3. Once order is placed order data will be stored in central DB and will be fragmented into local region DB
4. Open PostgreSQL to see the distributed data

-----------------PART3----------------
Query Optimization

1. The Database architecture of fragmented DBs and central DB optimizes the retrieval of data
2. Access the Sales data through Admin Profile
3. The sales data will display data from central db and instead data retrieval from local dbs to reduce latency by avoiding joins

-----------------PART4----------------
ACID Properties

-. Atomicity:
1. Add products in User Profile
2. If components exist in the data only then product will be added to DB
3. This ensures Atomicity

- Consistency
1. Logical checks for product quantity and component quantity are in place for customer orders
2. Invalid quantity will not place order
3. This ensures consistency in data

- Isolation
1. Region data for Inventory, Products and suppliers are isolated into different DBs
2. In user profile we select region and then execute insert functions in above mentioned tables
3. Data is isolated into specified regions
4. This ensures Isolation

-----------------PART5----------------
Usage of No SQL 

1. Add product in user profile
2. This will create a product-component mapping in MongoDB 
3. Order-Product Mapping is also created using NoSQL after placing orders in customer profile


