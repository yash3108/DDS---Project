-- Global Tables

CREATE TABLE IF NOT EXISTS Customers
(
  customer_id SERIAL,
  name        TEXT    NOT NULL,
  country     TEXT    NOT NULL,
  region      TEXT    NOT NULL,
  PRIMARY KEY (customer_id)
);


CREATE TABLE IF NOT EXISTS Orders
(
  order_id    SERIAL,
  customer_id INTEGER  NOT NULL,
  order_date  DATE,
  status      TEXT    ,
  region      TEXT NOT NULL
)
PARTITION BY LIST (region);


CREATE EXTENSION IF NOT EXISTS postgres_fdw;

CREATE SERVER IF NOT EXISTS boston_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'boston_db', host 'localhost');

CREATE USER MAPPING IF NOT EXISTS FOR current_user SERVER boston_server OPTIONS (user 'postgres', password 'postgres');

CREATE SERVER IF NOT EXISTS denver_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'denver_db', host 'localhost');

CREATE USER MAPPING IF NOT EXISTS FOR current_user SERVER denver_server OPTIONS (user 'postgres', password 'postgres');

CREATE SERVER IF NOT EXISTS seattle_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'seattle_db', host 'localhost');

CREATE USER MAPPING  IF NOT EXISTS FOR current_user SERVER seattle_server OPTIONS (user 'postgres', password 'postgres');
  
CREATE FOREIGN TABLE IF NOT EXISTS orders_boston PARTITION OF Orders
    FOR VALUES IN ('boston')
    SERVER boston_server OPTIONS (table_name 'orders');

CREATE FOREIGN TABLE IF NOT EXISTS orders_denver PARTITION OF Orders
    FOR VALUES IN ('denver')
    SERVER denver_server OPTIONS (table_name 'orders');

CREATE FOREIGN TABLE IF NOT EXISTS orders_seattle PARTITION OF Orders
    FOR VALUES IN ('seattle')
    SERVER seattle_server OPTIONS (table_name 'orders');    


  -- ALTER TABLE map_product_component
  --   ADD CONSTRAINT FK_Products_TO_map_product_component
  --     FOREIGN KEY (product_id)
  --     REFERENCES Products (product_id);

  -- ALTER TABLE map_product_component
  --   ADD CONSTRAINT FK_Components_TO_map_product_component
  --     FOREIGN KEY (component_id)
  --     REFERENCES Components (component_id);

-- ALTER TABLE Orders
--   ADD CONSTRAINT FK_Customer_TO_Orders
--     FOREIGN KEY (customer_id)
--     REFERENCES Customer (customer_id);

-- ALTER TABLE map_order_product
--   ADD CONSTRAINT FK_Orders_TO_map_order_product
--     FOREIGN KEY (order_id)
--     REFERENCES Orders (order_id);

-- ALTER TABLE map_order_product
--   ADD CONSTRAINT FK_Products_TO_map_order_product
--     FOREIGN KEY (product_id)
--     REFERENCES Products (product_id);

-- ALTER TABLE Products
--   ADD CONSTRAINT FK_Inventory_TO_Products
--     FOREIGN KEY (inventory_id)
--     REFERENCES Inventory (inventory_id);

-- ALTER TABLE Components
--   ADD CONSTRAINT FK_Suppliers_TO_Components
--     FOREIGN KEY (supplier_id)
--     REFERENCES Suppliers (supplier_id);

-- ALTER TABLE Components
--   ADD CONSTRAINT FK_Inventory_TO_Components
--     FOREIGN KEY (inventory_id)
--     REFERENCES Inventory (inventory_id);

-- insert into Components (component_id, name, description, date_created, quantity_available, price, supplier_id, inventory_id) values (1, 'Integrated Circuits', 'Chips', '10/22/2023', 92, 20, 3, 2);
-- insert into Components (component_id, name, description, date_created, quantity_available, price, supplier_id, inventory_id) values (2, 'Motherboard', 'Processor of the product', '04/15/2023', 55, 100, 2, 3);
-- insert into Components (component_id, name, description, date_created, quantity_available, price, supplier_id, inventory_id) values (3, 'Resistors', 'Component', '02/17/2023', 79, 2, 5, 3);
-- insert into Components (component_id, name, description, date_created, quantity_available, price, supplier_id, inventory_id) values (4, 'Diodes', 'Component', '12/23/2022', 36, 3, 2, 2);
-- insert into Components (component_id, name, description, date_created, quantity_available, price, supplier_id, inventory_id) values (5, 'Switch', 'Used for Toggle', '08/30/2023', 61, 10, 4, 1);
-- insert into Components (component_id, name, description, date_created, quantity_available, price, supplier_id, inventory_id) values (6, 'Transistors', 'Component', '12/07/2022', 33, 4, 3, 3);
-- insert into Components (component_id, name, description, date_created, quantity_available, price, supplier_id, inventory_id) values (7, 'Analog Circuits', 'Chips', '10/25/2023', 97, 20, 1, 3);
-- insert into Components (component_id, name, description, date_created, quantity_available, price, supplier_id, inventory_id) values (8, 'Clock', 'Used to maintain time', '02/06/2023', 78, 15, 1, 1);

-- insert into Suppliers (supplier_id, name, country) values (1, 'AP Supplier', 'United States');
-- insert into Suppliers (supplier_id, name, country) values (2, 'HS Industries', 'Germany');
-- insert into Suppliers (supplier_id, name, country) values (3, 'DPM', 'Japan');
-- insert into Suppliers (supplier_id, name, country) values (4, 'NMS', 'United States');
-- insert into Suppliers (supplier_id, name, country) values (5, 'HDNA', 'Brazil');

-- insert into Inventory (inventory_id, country, last_updated) values (1, 'Taiwan', '8/4/2023');
-- insert into Inventory (inventory_id, country, last_updated) values (2, 'Germany', '1/18/2023');
-- insert into Inventory (inventory_id, country, last_updated) values (3, 'Germany', '1/8/2023');

-- insert into Customer (customer_id, name, country) values (1, 'Yabox', 'China');
-- insert into Customer (customer_id, name, country) values (2, 'Tagcat', 'Indonesia');
-- insert into Customer (customer_id, name, country) values (3, 'Jabbersphere', 'China');
-- insert into Customer (customer_id, name, country) values (4, 'Mydo', 'China');
-- insert into Customer (customer_id, name, country) values (5, 'Zoomdog', 'Vietnam');
-- insert into Customer (customer_id, name, country) values (6, 'Aibox', 'Philippines');
-- insert into Customer (customer_id, name, country) values (7, 'Jazzy', 'Israel');
-- insert into Customer (customer_id, name, country) values (8, 'Topicshots', 'Botswana');
-- insert into Customer (customer_id, name, country) values (9, 'Tazzy', 'Czech Republic');
-- insert into Customer (customer_id, name, country) values (10, 'Livetube', 'France');