DROP TABLE IF EXISTS schedule;

CREATE TABLE schedule (
    day TEXT PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    plan TEXT NOT NULL,
    sleep TEXT,
    actual TEXT,
    notes TEXT
);
