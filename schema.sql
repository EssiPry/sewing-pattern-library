CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);  
CREATE TABLE patterns (id SERIAL PRIMARY KEY, name TEXT UNIQUE, company TEXT, fabric INTEGER); 
