CREATE DOMAIN email_address AS VARCHAR (255)
    CHECK (VALUE ~ '^[a-zA-ZO-9._%+-]+@[a-zA-ZO-9.-]+|. [a-zA-Z]{2, }$');
	
CREATE DOMAIN phone_number AS VARCHAR (20)
    CHECK (VALUE ~ '^|+?[0-9()-]+|s?[0-9]*$');

CREATE DOMAIN address AS VARCHAR (255)
    CHECK (VALUE ~ '^[a-zA-ZO-9.,\s-]+$');
	
CREATE TABLE customers(
    customer_id INT GENERATED ALWAYS AS IDENTITY, 
	customer_name VARCHAR(50) NOT NULL UNIQUE, 
	address address NOT NULL UNIQUE, 
	bank_account VARCHAR(50) NOT NULL UNIQUE, 
	PRIMARY KEY(customer_id)
);

CREATE TABLE responsible_persons (
    responsible_person_id INT GENERATED ALWAYS AS IDENTITY, 
	first_name VARCHAR(30) NOT NULL, 
	last_name VARCHAR(30) NOT NULL, 
	phone_number phone_number NOT NULL,
	email email_address NOT NULL, 
	PRIMARY KEY (responsible_person_id),
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE suppliers(
    supplier_id INT GENERATED ALWAYS AS IDENTITY, 
	supplier_name VARCHAR(30) NOT NULL, 
	phone_number phone_number NOT NULL UNIQUE,
	address address,
	email email_address NOT NULL UNIQUE, 
    PRIMARY KEY (supplier_id)
);

CREATE TABLE goods (
    good_id INT GENERATED ALWAYS AS IDENTITY, 
    good_name VARCHAR(30) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (good_id)
);

CREATE TABLE properties (
    property_id INT GENERATED ALWAYS AS IDENTITY, 
	color VARCHAR(50) NOT NULL,
	size_ INT NOT NULL,
	manufacturer VARCHAR(100) NOT NULL,
	material VARCHAR(100) NOT NULL,
	PRIMARY KEY (property_id),
    good_id INT REFERENCES goods(good_id) ON DELETE CASCADE
);

CREATE TABLE orders(
    order_id INT GENERATED ALWAYS AS IDENTITY, 
	total_price DECIMAL(10, 2) NOT NULL, 
	delivery_method VARCHAR(50) NOT NULL,
	PRIMARY KEY (order_id),
	customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE order_goods (
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,
    good_id INT REFERENCES goods(good_id) ON DELETE CASCADE,
    PRIMARY KEY (order_id, good_id)
);

CREATE TABLE goods_suppliers (
    good_id INT REFERENCES goods(good_id) ON DELETE CASCADE,
    supplier_id INT REFERENCES suppliers(supplier_id) ON DELETE CASCADE,
    PRIMARY KEY (good_id, supplier_id)
);

