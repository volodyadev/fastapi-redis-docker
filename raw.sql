-- Создание таблиц
CREATE TABLE IF NOT EXISTS short_names (
    name TEXT PRIMARY KEY,
    status INTEGER
);

CREATE TABLE IF NOT EXISTS full_names (
    name TEXT PRIMARY KEY,
    status INTEGER
);

-- Создание функции для генерации случайного расширения файла (три случайных символа)
CREATE OR REPLACE FUNCTION generate_file_extension()
RETURNS TEXT AS $$
BEGIN
    RETURN substring(md5(random()::text || clock_timestamp()::text), 1, 3);
END;
$$ LANGUAGE plpgsql;

-- Население таблицы short_names случайными данными
DO $$
DECLARE
    random_extension TEXT;
    random_status INTEGER;
    random_name TEXT;
BEGIN
    FOR i IN 1..700000 LOOP
        -- Генерация случайного расширения файла
        random_extension := generate_file_extension();
        
        -- Генерация случайного статуса (0 или 1)
        random_status := floor(random() * 2);
        
        -- Генерация случайного имени файла с добавлением расширения
        random_name := (SELECT substring(md5(random()::text || clock_timestamp()::text), 1, 15)) || '.' || random_extension;
        
        -- Вставка записи в таблицу short_names
        INSERT INTO short_names (name, status)
        VALUES (random_name, random_status);
    END LOOP;
END;
$$;

-- Население таблицы full_names случайными данными из short_names
INSERT INTO full_names (name)
SELECT name
FROM short_names
ORDER BY random()
LIMIT 500000;

-- Удаляем расширения в short_names
UPDATE short_names
SET name = regexp_replace(name, '\..*$', '');


-- Запрос для наполнения статусов full_names (Вариант 1)
-- UPDATE full_names fn
-- SET status = sn.status
-- FROM short_names sn
-- WHERE substring(fn.name, 1, length(fn.name) - 4) = sn.name;

-- Запрос для наполнения статусов full_names (Вариант 2) 
UPDATE full_names fn
SET status = (
    SELECT sn.status
    FROM short_names sn
    WHERE substring(fn.name, 1, length(fn.name) - 4) = sn.name
);

--  Проверяем корректность вставки 
SELECT *
FROM short_names s
LEFT JOIN full_names f ON s.name = substring(f.name, 1, length(f.name) - 4);