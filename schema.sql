DROP TABLE IF EXISTS schedules;
DROP TABLE IF EXISTS events;

CREATE TABLE employee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);


CREATE TABLE plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    station TEXT,
    last_worked TEXT,
    assigned BOOLEAN,
    FOREIGN KEY (employee_id) REFERENCES employee (id) ON DELETE CASCADE
);
