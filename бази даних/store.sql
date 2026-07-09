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
VALUES 
('Customer 1', '123 Main St, City, Country', '12345678901234'),
('Customer 2', '456 Elm St, Town, Country', '56789012345678'),
('Customer 3', '789 Oak St, Village, Country', '98765432109876'),
('Customer 4', '321 Pine St, Town, Country', '54321098765432'),
('Customer 5', '654 Maple St, City, Country', '67890123456789');

-- Inserting data into the responsible_persons table
INSERT INTO responsible_persons (first_name, last_name, phone_number, email, customer_id) 
VALUES 
('John', 'Doe', '1234567890', 'john@example.com', 1),
('Jane', 'Smith', '9876543210', 'jane@example.com', 2),
('Emily', 'Johnson', '1112223333', 'emily@example.com', 3),
('Michael', 'Brown', '4445556666', 'michael@example.com', 4),
('Sarah', 'Davis', '7778889999', 'sarah@example.com', 5);

-- Inserting data into the suppliers table
INSERT INTO suppliers (supplier_name, phone_number, address, email) 
VALUES 
('Supplier 1', '1112223333', '789 Oak St, Village, Country', 'supplier1@example.com'),
('Supplier 2', '4445556666', '321 Pine St, Town, Country', 'supplier2@example.com'),
('Supplier 3', '9998887777', '654 Maple St, City, Country', 'supplier3@example.com'),
('Supplier 4', '5554443333', '876 Birch St, Town, Country', 'supplier4@example.com'),
('Supplier 5', '3332221111', '123 Cedar St, Village, Country', 'supplier5@example.com');

-- Inserting data into the goods table
INSERT INTO goods (good_name, price) 
VALUES 
('Good 1', 10.99),
('Good 2', 20.50),
('Good 3', 15.75),
('Good 4', 5.25),
('Good 5', 50.00);

-- Inserting data into the properties table
INSERT INTO properties (color, size_, manufacturer, material, good_id) 
VALUES 
('Red', 10, 'ABC Manufacturing', 'Cotton', 1),
('Blue', 12, 'XYZ Company', 'Wool', 2),
('Green', 8, 'LMN Corp', 'Silk', 3),
('Yellow', 6, 'OPQ Industries', 'Polyester', 4),
('Black', 14, 'RST Enterprises', 'Leather', 5);

-- Inserting data into the orders table
INSERT INTO orders (total_price, delivery_method, customer_id) 
VALUES 
(50.00, 'Express', 1),
(75.50, 'Standard', 2),
(20.00, 'Express', 3),
(100.75, 'Standard', 4),
(150.00, 'Express', 5);

-- Inserting data into the order_goods table
INSERT INTO order_goods (order_id, good_id) 
VALUES 
(1, 1),
(1, 2),
(2, 3),
(3, 4),
(4, 5),
(5, 1),
(5, 3);

-- Inserting data into the goods_suppliers table
INSERT INTO goods_suppliers (good_id, supplier_id) 
VALUES 
(1, 1),
(1, 2),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- Створення індексу для одного стовпчика + демонстація
CREATE INDEX idx_customers_customer_name ON customers(customer_name);
EXPLAIN ANALYZE SELECT * FROM customers WHERE customer_name = 'Customer 1';

-- Створення складеного (багатостовпчикового) індексу + демонстація
CREATE INDEX idx_responsible_persons_name_phone ON responsible_persons(first_name, last_name, phone_number);
EXPLAIN ANALYZE SELECT * FROM responsible_persons WHERE first_name = 'John' AND last_name = 'Doe' AND phone_number = '1234567890';

-- Створення унікального індексу + демонстація
CREATE UNIQUE INDEX idx_suppliers_email_unique ON suppliers(email);
EXPLAIN ANALYZE SELECT * FROM suppliers WHERE email = 'supplier1@example.com';

-- Створення індексу за виразом (наприклад, для нижнього регістру імені постачальника) + демонстація
CREATE INDEX idx_goods_name_lower ON goods(LOWER(good_name));
EXPLAIN ANALYZE SELECT * FROM goods WHERE LOWER(good_name) = 'good 1';

-- Створення часткового індексу (наприклад, для замовлень з певним методом доставки) + демонстація
CREATE INDEX idx_orders_express_only ON orders(delivery_method) WHERE delivery_method = 'Express';
EXPLAIN ANALYZE SELECT * FROM orders WHERE delivery_method = 'Express';


--- Для порівняння часу виконання без індексу ---
DROP INDEX IF EXISTS idx_customers_customer_name;
EXPLAIN ANALYZE SELECT * FROM customers WHERE customer_name = 'Customer 1';
---

--- Функція, яка приймає параметри і повертає одну стрічку типу RECORD
CREATE OR REPLACE FUNCTION get_order_info(p_order_id INT)
RETURNS TABLE (
    order_id INT,
    customer_name VARCHAR(50),
    total_price DECIMAL(10, 2),
    delivery_method VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY
    SELECT o.order_id, c.customer_name, o.total_price, o.delivery_method
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_id = p_order_id;
END;
$$ LANGUAGE plpgsql;

-- Використання:
SELECT * FROM get_order_info(1);

--- Функція, яка приймає складний тип даних (SETOF), повертає список товарів, поставлених конкретним постачальником
CREATE OR REPLACE FUNCTION get_supplier_goods(p_supplier_id INT)
RETURNS TABLE (
    good_id INT,
    good_name VARCHAR(30),
    price NUMERIC(10, 2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT g.good_id, g.good_name, g.price
    FROM goods g
    JOIN goods_suppliers gs ON g.good_id = gs.good_id
    WHERE gs.supplier_id = p_supplier_id;
END;
$$ LANGUAGE plpgsql;


-- Використання:
SELECT * FROM get_supplier_goods(1);


--- Функція з підзапитом, яка повертає таблицю всіх клієнтів з кількістю їхніх замовлень
CREATE OR REPLACE FUNCTION get_customers_order_count()
RETURNS TABLE (
    customer_name VARCHAR,
    order_count INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.customer_name, COUNT(o.order_id)::INTEGER AS order_count
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_name;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_customers_order_count();

--- Змінюване представлення (з використанням CHECK OPTION)
CREATE OR REPLACE VIEW express_orders AS
SELECT * FROM orders
WHERE delivery_method = 'Express'
WITH CHECK OPTION;
--успішно
INSERT INTO express_orders (total_price, delivery_method, customer_id)
VALUES (60.00, 'Express', 1);  -- Це буде успішно, оскільки метод доставки - 'Express'
--неуспішно
INSERT INTO express_orders (total_price, delivery_method, customer_id)
VALUES (70.00, 'Standard', 2);  -- Це не буде успішно, оскільки метод доставки не 'Express'

UPDATE express_orders
SET total_price = 57.00
WHERE order_id = 1;  -- Це успішно, якщо order_id = 1 і метод доставки - 'Express'

--- Незмінюване представлення
CREATE OR REPLACE VIEW customer_orders AS
SELECT c.customer_name, o.order_id, o.total_price
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

SELECT * FROM customer_orders;

--- Матеріалізоване представлення
CREATE MATERIALIZED VIEW order_summary AS
SELECT o.order_id, COUNT(og.good_id) AS goods_count, SUM(g.price) AS total_goods_price
FROM orders o
JOIN order_goods og ON o.order_id = og.order_id
JOIN goods g ON og.good_id = g.good_id
GROUP BY o.order_id;

SELECT * FROM order_summary;

REFRESH MATERIALIZED VIEW order_summary;
SELECT * FROM order_summary;



--- Ця процедура дозволяє перевірити існування замовлення, 
--- вивести загальну ціну та перерахувати всі товари, що входять до замовлення.
CREATE OR REPLACE PROCEDURE process_order(p_order_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_order RECORD;
    v_total_price DECIMAL(10, 2);
    v_delivery_method VARCHAR(50);
    v_good_name VARCHAR(30);
    v_good_price DECIMAL(10, 2);
    v_cursor CURSOR FOR
        SELECT g.good_name, g.price
        FROM goods g
        JOIN order_goods og ON g.good_id = og.good_id
        WHERE og.order_id = p_order_id;
BEGIN
    -- Отримуємо нформацію про замовлення
    SELECT o.total_price, o.delivery_method
    INTO v_total_price, v_delivery_method
    FROM orders o
    WHERE o.order_id = p_order_id;
    
    -- Перевіряємо, чи існує замовлення з таким ID
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Order ID % does not exist.', p_order_id;
    END IF;

    -- Виводимо загальну ціну та метод доставки замовлення
    RAISE NOTICE 'Total price for order %: %, Delivery method: %', p_order_id, v_total_price, v_delivery_method;

    -- Відкриваємо курсор і обробляємо кожен товар
    OPEN v_cursor;
    LOOP
        FETCH v_cursor INTO v_order;
        EXIT WHEN NOT FOUND;

        v_good_name := v_order.good_name;
        v_good_price := v_order.price;

        -- Виводимо інформацію про товар
        RAISE NOTICE 'Good name: %, Price: %', v_good_name, v_good_price;
    END LOOP;

    CLOSE v_cursor;

EXCEPTION
    WHEN others THEN
        RAISE NOTICE 'An error occurred: %', SQLERRM;
END;
$$;

CALL process_order(2);


--- Ця процедура перевіряє, чи існує постачальник, 
--- обчислює загальну ціну товарів, що постачаються цим постачальником, 
--- і виводить інформацію про кожен товар.
CREATE OR REPLACE PROCEDURE process_supplier_goods(p_supplier_id INT)
LANGUAGE plpgsql
AS $$
DECLARE
    v_good RECORD;
    v_total_price DECIMAL(10, 2);
    v_cursor CURSOR FOR
        SELECT g.good_id, g.good_name, g.price
        FROM goods g
        JOIN goods_suppliers gs ON g.good_id = gs.good_id
        WHERE gs.supplier_id = p_supplier_id;
BEGIN
    -- Перевірка наявності постачальника
    IF NOT EXISTS (
        SELECT 1 FROM suppliers WHERE supplier_id = p_supplier_id
    ) THEN
        RAISE EXCEPTION 'Supplier ID % does not exist.', p_supplier_id;
    END IF;

    -- Виведення загальної ціни товарів постачальника (використання SUM)
    SELECT SUM(g.price)
    INTO v_total_price
    FROM goods g
    JOIN goods_suppliers gs ON g.good_id = gs.good_id
    WHERE gs.supplier_id = p_supplier_id;

    -- Виведення загальної ціни
    RAISE NOTICE 'Total price of goods supplied by supplier %: %', p_supplier_id, v_total_price;

    -- Обробка курсором
    OPEN v_cursor;
    LOOP
        FETCH v_cursor INTO v_good;
        EXIT WHEN NOT FOUND;

        -- Виведення інформації про товар
        RAISE NOTICE 'Good ID: %, Good name: %, Price: %', v_good.good_id, v_good.good_name, v_good.price;
    END LOOP;

    CLOSE v_cursor;

EXCEPTION
    WHEN others THEN
        RAISE NOTICE 'An error occurred: %', SQLERRM;
END;
$$;

CALL process_supplier_goods(1);












-----------------------------------------------------------------
-- Функція для отримання загальної суми товарів в замовленні
CREATE OR REPLACE FUNCTION calculate_order_total(p_order_id INT)
RETURNS DECIMAL(10, 2) AS $$
DECLARE
    v_total DECIMAL(10, 2);
BEGIN
    SELECT SUM(g.price)
    INTO v_total
    FROM goods g
    JOIN order_goods og ON g.good_id = og.good_id
    WHERE og.order_id = p_order_id;

    RETURN v_total;
END;
$$ LANGUAGE plpgsql;



SELECT o.order_id,
       o.total_price AS recorded_total_price,
       COALESCE(SUM(g.price), 0) AS calculated_total_price
FROM orders o
LEFT JOIN order_goods og ON o.order_id = og.order_id
LEFT JOIN goods g ON og.good_id = g.good_id
GROUP BY o.order_id, o.total_price;


SELECT * FROM goods;

-- Розрахунок правильної загальної суми для кожного замовлення
WITH calculated_totals AS (
    SELECT 
        o.order_id,
        SUM(g.price) AS calculated_total_price
    FROM 
        orders o
    JOIN 
        order_goods og ON o.order_id = og.order_id
    JOIN 
        goods g ON og.good_id = g.good_id
    GROUP BY 
        o.order_id
)
SELECT * FROM calculated_totals;


-- Оновлення загальної суми у таблиці orders
WITH calculated_totals AS (
    SELECT 
        o.order_id,
        SUM(g.price) AS calculated_total_price
    FROM 
        orders o
    JOIN 
        order_goods og ON o.order_id = og.order_id
    JOIN 
        goods g ON og.good_id = g.good_id
    GROUP BY 
        o.order_id
)
UPDATE orders
SET total_price = ct.calculated_total_price
FROM calculated_totals ct
WHERE orders.order_id = ct.order_id;


-- Перевірка результатів
SELECT 
    o.order_id,
    o.total_price AS recorded_total_price,
    ct.calculated_total_price
FROM 
    orders o
JOIN 
    calculated_totals ct ON o.order_id = ct.order_id;
