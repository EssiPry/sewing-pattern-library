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

def add_garment_type_to_pattern(pattern_id, garment_id):
    pattern_id=pattern_id
    garment_id=garment_id
    sql= "INSERT INTO garments_in_pattern (pattern_id, garment_id) VALUES (:pattern_id, :garment_id)"
    db.session.execute(sql, {"pattern_id":pattern_id, "garment_id":garment_id})
    db.session.commit()

def get_patterns_by_name(name):
    name = name 
    sql = "SELECT * FROM patterns WHERE name LIKE :name"
    return db.session.execute(sql, {"name":"%"+name+"%"}).fetchall()

def get_pattern_by_name(name):
    name = name
    sql = "SELECT * FROM patterns WHERE name = :name"
    return db.session.execute(sql, {"name":name}).fetchone()

def count_by_name(name):
    name = name
    sql ="SELECT COUNT(*) FROM patterns WHERE name LIKE :name"
    return db.session.execute(sql, {"name":"%"+name+"%"}).fetchone()[0]

def get_pattern_id(name):
    name = name
    sql ="SELECT id FROM patterns WHERE name = :name"
    return db.session.execute(sql, {"name":name}).fetchone()[0]

def get_garment_id(garment):
    garment=garment
    sql ="SELECT id FROM garments WHERE garment = :garment"
    return db.session.execute(sql, {"garment":garment}).fetchone()[0]