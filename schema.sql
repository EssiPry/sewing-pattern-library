CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);  
CREATE TABLE patterns (id SERIAL PRIMARY KEY, name TEXT UNIQUE, company TEXT, fabric INTEGER); 
CREATE TABLE reviews (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, pattern_id INTEGER REFERENCES patterns, review TEXT, date DATE); 

