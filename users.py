from db import db 
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv


def login(username, password):
    sql = "SELECT id, username, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else: 
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.username
            return True 
        return False

def logout():
    del session["user_id"]
    del session["user_name"]

def register(username, password): 
    hash_value = generate_password_hash(password)
    try: 
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False
