import secrets
from os import getenv
from db import db
from flask import abort, session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT id, username, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["user_name"] = user.username
        session["csrf_token"] = secrets.token_hex(16)
        session["logged_in"] = True
        return True
    return False

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["csrf_token"]
    del session["logged_in"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
        return True
    except:
        return False

def get_user_id():
    return session.get("user_id")

def check_csrf(csrf):
    if session["csrf_token"] != csrf:
        abort(403)
