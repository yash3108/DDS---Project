INSERT INTO Customers (name, country, region) VALUES ('Albert LLC', 'Japan', 'seattle');
INSERT INTO Customers (name, country, region) VALUES ('Brite LLC', 'Canada', 'denver');
INSERT INTO Customers (name, country, region) VALUES ('Champ LLC', 'UK', 'boston');
INSERT INTO Customers (name, country, region) VALUES ('Drake LLC', 'Germany', 'seattle');

INSERT INTO ORDERS (customer_id, order_date, status, region) VALUES (1,'2020-02-01', 'placed', 'seattle');
INSERT INTO ORDERS (customer_id, order_date, status, region) VALUES (2,'2020-12-10', 'placed', 'denver');
INSERT INTO ORDERS (customer_id, order_date, status, region) VALUES (3,'2020-09-01', 'placed', 'seattle');
INSERT INTO ORDERS (customer_id, order_date, status, region) VALUES (4,'2020-01-09', 'placed', 'boston');

COMMIT;


