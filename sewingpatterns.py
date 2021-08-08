from db import db
from flask import session

def get_all_patterns():
    sql = "SELECT * FROM patterns"
    return db.session.execute(sql).fetchall()

def count_all_patterns(): 
    sql = "SELECT COUNT(*) FROM patterns"
    return db.session.execute(sql).fetchone()[0]

def get_pattern_by_name(name):
    name = name 
    sql = "SELECT * FROM patterns WHERE name LIKE :name"
    return db.session.execute(sql, {"name":"%"+name+"%"}).fetchall()

def count_by_name(name):
    name = name
    sql ="SELECT COUNT(*) FROM patterns WHERE name LIKE :name"
    return db.session.execute(sql, {"name":"%"+name+"%"}).fetchone()[0]

