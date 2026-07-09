-- transaction D
BEGIN;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Додавання ще одного нового клієнта
INSERT INTO customers (customer_name, address, bank_account) 
VALUES ('Customer 9', '892 Main St, Dnipro, Ukraine', '44453566966666');

-- Збереження точки
SAVEPOINT before_responsible_person;

-- Спроба додати відповідальну особу для клієнта, яка може спричинити конфлікт
INSERT INTO responsible_persons (first_name, last_name, phone_number, email, customer_id) 
VALUES ('Sam', 'Guk', '0987634321', 'sam@example.com', currval('customers_customer_id_seq'));

-- Відкат до точки збереження у випадку конфлікту
ROLLBACK TO SAVEPOINT before_responsible_person;

-- Фіксація транзакції
COMMIT;


-- Перевірка таблиці customers
SELECT * FROM customers;

-- Перевірка таблиці responsible_persons
SELECT * FROM responsible_persons;