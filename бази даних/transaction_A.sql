
-- transaction A
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- Оновлення ціни товару
UPDATE goods
SET price = price * 1.10
WHERE good_name = 'Good 1';

-- Збереження точки
SAVEPOINT before_discount;

-- Додаткове оновлення для застосування знижки
UPDATE goods
SET price = price * 0.90
WHERE good_name = 'Good 2';

-- Фіксація транзакції
COMMIT;

-- Перевірка таблиці goods
SELECT * FROM goods;
