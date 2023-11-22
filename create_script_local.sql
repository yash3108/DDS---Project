CREATE TABLE IF NOT EXISTS Inventory
(
  component_id       SERIAL,
  name               TEXT     NOT NULL,
  description        TEXT    ,
  date_created       DATE NOT NULL,
  quantity INTEGER  NOT NULL DEFAULT 0,
  price              INTEGER   NOT NULL,
  PRIMARY KEY (component_id)
);


CREATE TABLE IF NOT EXISTS Orders
(
  order_id    SERIAL,
  customer_id INTEGER  NOT NULL,
  order_date  DATE,
  status      TEXT    ,
  region_id   INTEGER NOT NULL, 
  PRIMARY KEY (order_id)
);

CREATE TABLE IF NOT EXISTS Products
(
  product_id         SERIAL,
  description        TEXT    ,
  date_created       DATE NOT NULL,
  price              INTEGER   NOT NULL,
  quantity           INTEGER  NOT NULL DEFAULT 0,
  PRIMARY KEY (product_id)
);