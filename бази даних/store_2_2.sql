DO $$ BEGIN
    CREATE DOMAIN email_address AS VARCHAR (255)
    CHECK (VALUE ~ '^[a-zA-ZO-9._%+-]+@[a-zA-ZO-9.-]+|. [a-zA-Z]{2, }$');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE DOMAIN phone_number AS VARCHAR (20)
    CHECK (VALUE ~ '^|+?[0-9()-]+|s?[0-9]*$');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE DOMAIN address AS VARCHAR (255)
    CHECK (VALUE ~ '^[a-zA-ZO-9.,\s-]+$');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS customers(
    customer_id INT GENERATED ALWAYS AS IDENTITY, 
	customer_name VARCHAR(50) NOT NULL UNIQUE, 
	address address NOT NULL UNIQUE, 
	bank_account VARCHAR(50) NOT NULL UNIQUE, 
	PRIMARY KEY(customer_id)
);

CREATE TABLE IF NOT EXISTS responsible_persons (
    responsible_person_id INT GENERATED ALWAYS AS IDENTITY, 
    first_name VARCHAR(30) NOT NULL, 
    last_name VARCHAR(30) NOT NULL, 
    phone_number phone_number NOT NULL,
    email email_address NOT NULL, 
    customer_id INT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    PRIMARY KEY (responsible_person_id)
);


CREATE TABLE IF NOT EXISTS suppliers(
    supplier_id INT GENERATED ALWAYS AS IDENTITY, 
	supplier_name VARCHAR(30) NOT NULL, 
	phone_number phone_number NOT NULL UNIQUE,
	address address,
	email email_address NOT NULL UNIQUE, 
    PRIMARY KEY (supplier_id)
);

CREATE TABLE IF NOT EXISTS goods (
    good_id INT GENERATED ALWAYS AS IDENTITY, 
    good_name VARCHAR(30) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (good_id)
);

CREATE TABLE IF NOT EXISTS properties (
    property_id INT GENERATED ALWAYS AS IDENTITY, 
	color VARCHAR(50) NOT NULL,
	size_ INT NOT NULL,
	manufacturer VARCHAR(100) NOT NULL,
	material VARCHAR(100) NOT NULL,
	PRIMARY KEY (property_id),
    good_id INT REFERENCES goods(good_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS orders(
    order_id INT GENERATED ALWAYS AS IDENTITY, 
	total_price DECIMAL(10, 2) NOT NULL, 
	delivery_method VARCHAR(50) NOT NULL,
	PRIMARY KEY (order_id),
	customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS order_goods (
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    good_id INT REFERENCES goods(good_id) ON DELETE CASCADE,
    PRIMARY KEY (order_id, good_id)
);

CREATE TABLE IF NOT EXISTS goods_suppliers (
    good_id INT REFERENCES goods(good_id) ON DELETE CASCADE,
    supplier_id INT REFERENCES suppliers(supplier_id) ON DELETE CASCADE,
    PRIMARY KEY (good_id, supplier_id)
);

-- Inserting data into the customers table
INSERT INTO customers (customer_name, address, bank_account) 
VALUES ('Customer 1', '123 Main St, City, Country', '12345678901234'),
       ('Customer 2', '456 Elm St, Town, Country', '56789012345678');

-- Inserting data into the responsible_persons table
INSERT INTO responsible_persons (first_name, last_name, phone_number, email, customer_id) 
VALUES ('John', 'Doe', '1234567890', 'john@example.com', 1),
       ('Jane', 'Smith', '9876543210', 'jane@example.com', 2);

-- Inserting data into the suppliers table
INSERT INTO suppliers (supplier_name, phone_number, address, email) 
VALUES ('Supplier 1', '1112223333', '789 Oak St, Village, Country', 'supplier1@example.com'),
       ('Supplier 2', '4445556666', '321 Pine St, Town, Country', 'supplier2@example.com');

-- Inserting data into the goods table
INSERT INTO goods (good_name, price) 
VALUES ('Good 1', 10.99),
       ('Good 2', 20.50);

-- Inserting data into the properties table
INSERT INTO properties (color, size_, manufacturer, material, good_id) 
VALUES ('Red', 10, 'ABC Manufacturing', 'Cotton', 1),
       ('Blue', 12, 'XYZ Company', 'Wool', 2);

-- Inserting data into the orders table
INSERT INTO orders (total_price, delivery_method, customer_id) 
VALUES (50.00, 'Express', 1),
       (75.50, 'Standard', 2);

-- Inserting data into the order_goods table
INSERT INTO order_goods (order_id, good_id) 
VALUES (1, 1),
       (1, 2),
       (2, 1);

-- Inserting data into the goods_suppliers table
INSERT INTO goods_suppliers (good_id, supplier_id) 
VALUES (1, 1),
       (1, 2),
       (2, 2);

