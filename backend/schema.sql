DROP TABLE IF EXISTS destinations;

-- TODO: You will need to modify the fields here
CREATE TABLE destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    photo TEXT NOT NULL,
    estimated_cost INTEGER NOT NULL,
    additional_info TEXT NOT NULL
);


