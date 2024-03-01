DROP TABLE IF EXISTS user;

CREATE TABLE user (
    name TEXT NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    points INTEGER NOT NULL
);

INSERT INTO user (name, id, points) VALUES
("Steve Smith", 211, 80),
("Jian Wong", 122, 92),
("Chris Peterson", 213, 91),
("Sai Patel", 524, 94),
("Andrew Whitehead", 425, 99),
("Lynn Roberts", 626, 90),
("Robert Sanders", 287, 75);