CREATE TABLE IF NOT EXISTS tables (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    game_name VARCHAR(255) NOT NULL
);


INSERT INTO tables (name, game_name) VALUES
(%s, %s)


UPDATE tables SET 
name = %s
game_name = %s
WHERE id = %s


DELETE FROM tables WHERE id = %s


SELECT * FROM tables


SELECT * FROM tables WHERE id = %s