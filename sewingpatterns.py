from db import db
from flask import session

def get_all_patterns():
    sql = "SELECT * FROM patterns"
    return db.session.execute(sql).fetchall()

def get_total_patterns(): 
    sql = "SELECT COUNT(*) FROM patterns"
    return db.session.execute(sql).fetchone()[0]

def get_pattern_by_name(name):
    sql = "SELECT * FROM patterns WHERE name=:name"
    return db.session.execute(sql, {"name":name}).fetchone()

