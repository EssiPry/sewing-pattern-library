from db import db 
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os 

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else: 
        return True 

def register(username, password): 
    hash_value = generate_password_hash(password)
    try: 
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False
