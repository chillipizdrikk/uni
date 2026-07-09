-- transaction B
BEGIN;
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Оновлення ціни іншого товару
UPDATE goods
SET price = price * 1.20
WHERE good_name = 'Good 4';

-- Збереження точки
SAVEPOINT before_discount;

-- Спроба застосувати знижку, яка може бути помилковою
UPDATE goods
SET price = price * 0.50
WHERE good_name = 'Good 5';

-- Відкат до точки збереження, якщо виникає помилка
ROLLBACK TO SAVEPOINT before_discount;

-- Фіксація транзакції
COMMIT;


-- Перевірка таблиці goods
SELECT * FROM goods;
