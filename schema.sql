CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);  
CREATE TABLE patterns (id SERIAL PRIMARY KEY, name TEXT UNIQUE, company TEXT, fabric TEXT); 
CREATE TABLE reviews (id SERIAL PRIMARY KEY, user_id INTEGER REFERENCES users, pattern_id INTEGER REFERENCES patterns, review TEXT, date DATE); 
CREATE TABLE garments (id SERIAL PRIMARY KEY, garment TEXT); 
CREATE TABLE garments_in_pattern (id SERIAL PRIMARY KEY, pattern_id INTEGER REFERENCES patterns, garment_id INTEGER REFERENCES garments); 

