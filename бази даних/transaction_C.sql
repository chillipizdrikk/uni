-- transaction C
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Додавання нового клієнта
INSERT INTO customers (customer_name, address, bank_account) 
VALUES ('Customer 8', '752 Main St, Lviv, Ukraine', '11382233933333');

-- Збереження точки
SAVEPOINT before_responsible_person;

-- Додавання відповідальної особи для нового клієнта
INSERT INTO responsible_persons (first_name, last_name, phone_number, email, customer_id) 
VALUES ('Kate', 'Trum', '1234567890', 'kate@example.com', currval('customers_customer_id_seq'));

-- Фіксація транзакції
COMMIT;


-- Перевірка таблиці customers
SELECT * FROM customers;

-- Перевірка таблиці responsible_persons
SELECT * FROM responsible_persons;
