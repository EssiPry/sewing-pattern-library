from db import db
from flask import session

def add_pattern_to_db(name, company, fabric):
    try: 
        sql = "INSERT INTO patterns (name, company, fabric) VALUES (:name, :company, :fabric)"
        db.session.execute(sql, {"name":name, "company":company, "fabric":fabric})
        db.session.commit()
        return True 
    except: 
        return False 

def get_patterns_by_name(name):
    name = name 
    sql = "SELECT * FROM patterns WHERE name LIKE :name"
    return db.session.execute(sql, {"name":"%"+name+"%"}).fetchall()

def count_by_name(name):
    name = name
    sql ="SELECT COUNT(*) FROM patterns WHERE name LIKE :name"
    return db.session.execute(sql, {"name":"%"+name+"%"}).fetchone()[0]

def get_pattern_by_name(name):
    name = name
    sql = "SELECT * FROM patterns WHERE name = :name"
    return db.session.execute(sql, {"name" : name}).fetchone()