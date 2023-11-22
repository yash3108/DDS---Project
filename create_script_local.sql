CREATE TABLE IF NOT EXISTS Inventory
(
  component_id       SERIAL,
  name               TEXT     NOT NULL,
  description        TEXT    ,
  date_created       DATETIME NOT NULL,
  quantity INTEGER  NOT NULL DEFAULT 0,
  price              DOUBLE   NOT NULL,
  PRIMARY KEY (component_id)
);


CREATE TABLE IF NOT EXISTS Orders
(
  order_id    SERIAL,
  customer_id INTEGER  NOT NULL,
  order_date  DATETIME,
  status      TEXT    ,
  region_id   INTEGER NOT NULL 
  PRIMARY KEY (order_id)
);

CREATE TABLE IF NOT EXISTS Products
(
  product_id         SERIAL,
  description        TEXT    ,
  date_created       DATETIME NOT NULL,
  price              DOUBLE   NOT NULL,
  quantity           INTEGER  NOT NULL DEFAULT 0,
  PRIMARY KEY (product_id)
);